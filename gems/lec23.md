### 1. Shadowing for Crash Consistency (Review from Previous Lecture)
**Key Points**
- Shadowing maintains two copies of data: current and shadow.
- Reads always read the current copy; writes update the shadow copy then flip the shadow bit.
- The shadow bit is binary (0 or non-zero) ensuring atomic updates without undefined states.
- Requires twice the storage (for current + shadow copies).
- Requires many flushes to impose ordering constraints.
- Ordering and atomicity are key challenges with shadowing.

_No direct problem stated, but this example is fundamental to understand subsequent journaling._

---

### 2. Journaling (Logging) Basic Mechanics and Supremacy Clause
**Key Points**
- Logging records updates to a journal (log) before committing to actual data blocks.
- Committed entries in the log supersede the state on disk (log has precedence).
- Reading a block: if a valid committed log entry exists for that block, read from the log.
- If the prefix of the log contains any uncommitted entry, the entire suffix of the log after that entry is invalidated.
- Log entries have: type, location, payload, and a commit record.
- Append-only semantics: log entries are only appended; no in-place writes.
- Commit entries atomically indicate the entry is valid.

**Problem statements & Examples:**

1. Reading block 7:
   - Log contains an entry for block 7 with a valid commit.
   - Data block 7 on disk has an older version.
   - Question: From where do you read block 7?

**Solution:**
You read from the log because the committed log entry supersedes the data block on disk. But only if all earlier log entries are also committed (prefix property).

---

2. Reading block 6:
   - Log contains an entry for block 6 but commit is invalid or missing.
   - Data block 6 on disk exists.
   - Question: Where do you read block 6?

**Solution:**
You read from data blocks on disk because the log entry is not committed (invalid), so you ignore it.

_Summary: The "supremacy clause" is central for ensuring crash consistency via the log._

---

### 3. Happens Before Relationship and Commit Ordering in the Log
**Key Points**
- Happens-before relation is a mathematical partial order: if commit B has occurred, entry A that it depends on must also have occurred.
- To ensure atomicity, must impose ordering between entry and its commit (entry_i happens before commit_i).
- Flush operations between entry and commit enforce partial ordering.
- Flush also needed to impose order between consecutive entry-commit pairs? → No, it is not necessary to place a flush between each commit-entry pair (i.e., between commit_i and entry_i+1) for crash consistency.
- Allows some re-ordering of commits and entries to improve performance by reducing flushes.

**Problem:**
Diagram of entry-commit pairs with flushes between entry and commit, no flush needed between commit_i and entry_i+1.

**Solution:**
Partial order is E1 < C1 and C1 < E2 (transitive), so a flush between E1-C1 ensures ordering for the next entry.

_Summary: Understanding flush placement reduces the number of flushes needed compared to shadowing, optimizing performance while preserving ordering and atomicity._

---

### 4. Commit Mechanism #1: Sequential Write with Flushes
**Key Points**
- Write entry, then flush, then write commit, then flush.
- The flush enforces atomicity and ordering guarantees.
- Each entry and commit are written in separate blocks.
- Improvements over shadowing: fewer flushes and no doubling of storage.
- Still suboptimal from performance standpoint.

---

### 5. Commit Mechanism #2: Commit with Checksums (Group Commit)
**Key Points**
- Instead of just writing a commit bit, write a checksum of the entry as commit.
- Multiple entries can be grouped in a single commit with a checksum.
- Allows multiple entries and commits to be written in any order because the checksum validates correctness.
- Drastically reduces flushes and improves performance.
- Detects corrupted or erroneous commits (bit flips, cosmic rays).
- During recovery or read, stop at the first invalid entry detected by checksum mismatch.
- The entire suffix of log after invalid entry is discarded.

**Problem:**
- How to handle writes if commit or entry gets corrupted?
- How does checksum-based commit help?

**Solution:**
Checksum commit validates and detects corruption, enabling out-of-order writes within log blocks while preserving atomicity. Recovery uses checksum validation to process only valid entries.

_Summary: Checksums enable group commits and unordered writes, improving performance and reliability._

---

### 6. Handling Multiple Writes to Same Block in the Log
**Key Points**
- Logging multiple writes to the same block creates multiple entries in sequence.
- When reading, the entire log is scanned from oldest to newest.
- Last valid write (commit and entry) for the block is applied.
- Invalid entries terminate the scan and discard subsequent entries.

**Example question raised:**
- How to differentiate first and second write to same block?

**Professor's explanation:**
- Log is scanned sequentially applying writes. No need to differentiate; log ordering ensures correctness.

_Summary: Log replay applies all valid writes in order, crucial for consistency._

---

### 7. Log Merge Operation (when log is full)
**Key Points**
- Log is finite space; when full, must merge entries to actual data blocks.
- The merge iterates over committed entries, applying updates onto disk data blocks.
- The merge process is a series of multiple disk IO operations.
- If a crash occurs in the middle of merge, system remains consistent due to idempotent updates and recovery design.
- Idempotency: repeated application of an operation yields same result (critical property).
- After merge, the log is cleared.

**Problem/Question:**
- What happens if crash during log merge?
- Is system crash consistent?

**Solution:**
- Using idempotent writes and the prefix invalidation property, crash during merge leads to replay again on recovery without corruption.
- Recovery merges remaining entries from the log.

---

### 8. Atomic Log Clearing after Merge
**Key Points**
- After merging the log, log space must be freed by clearing the log.
- Atomic log clearing is done by invalidating only the first entry using a single atomic write (e.g., writing garbage checksum).
- Because logs are prefix invalidated at first invalid entry, no need to invalidate every entry.
- This single write ensures crash consistency in log clearing without complex multi-IO atomic actions.

**Problem:**
- How to atomically clear the log on disk?

**Solution:**
One atomic write that invalidates the first log entry (by corrupting checksum) suffices to mark whole log invalid.

---

### 9. Recovery Procedure
**Key Points**
- On startup: recover by merging the log.
- Merge applies valid entries and stops at first invalid entry.
- Afterwards, clear the log atomically by invalidating first entry.
- System is ready to use post recovery.

---

### 10. Benefits of Logging vs. Shadowing
**Key Points**
- Logging requires fewer flushes → better performance.
- Logging avoids doubling storage required by shadowing.
- Logging enables sequential disk access (append-only log) → greatly benefits spinning disks.
- Provides correctness: atomicity and ordering.
- Significant reduction or elimination of flushes/sync points.

---

### 11. Costs and Limitations of Logging
**Key Points**
- Double writes required: write to log then overwrite data blocks.
- Periodic log merge required to free log space.
- Merge can happen unpredictably → affects latency.
- Less predictable; problematic for latency-sensitive or real-time systems.
- No control over when merges happen → impacts soft real-time or mission critical apps.
- System designers must consider tradeoffs between safety and performance.

**Example exam hint:**
- "If I were to ask you whether logging is suitable for latency-sensitive systems, what would your answer be?" — logging is typically not suitable due to unpredictable latency spikes caused by log merges.

---

### 12. Modern File System Logging Types & Design Tradeoffs
**Key Points**
- Options: No logging (write-back), metadata-only logging, full logging (metadata + data), ordered logging.
- Ordered logging journals metadata only, but ensures data writes precede metadata writes.
- Tradeoff space spanned by safety vs. performance.
- No one best design; choices depend on application needs.
- Full journaling = high safety, low performance.
- Write-back = high performance, low safety.
- Ordered journaling strikes balance.

_Example question for next class: Where within the tradeoff space does ordered journaling fall?_

---

# Summary of Exam-Relevant Examples and Questions

- Reading from log vs. data blocks depending on commit validity and prefix property.
- Flush placement for atomicity and ordering (whether flush needed between commit_i and entry_i+1).
- Commit mechanism #1 (flush-based) and commit mechanism #2 (checksum-based).
- Handling corrupted/incomplete commits with checksum validation.
- How multiple writes to same block are logged and replayed.
- Log merge operation: how crash during merge is handled.
- Atomic clearing of the log with a single atomic write invalidating first entry.
- SOFT question: is logging suitable for latency sensitive (real-time) systems? (Answer: generally no, due to unpredictable log merges).
- Tradeoff space for journaling designs (write-back, full journaling, ordered journaling).

---

These examples and questions reflect the professor's emphasis on first-principles reasoning about atomicity, ordering, crash consistency, and performance tradeoffs in file system logging. Ensuring understanding of these mechanics and reasoning about ordering and atomicity with flushes, commits, and checksums is essential for exam preparation.