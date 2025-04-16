### 1. Crash Consistency Scenario with Single Write and Crash
**Key Points**
- Two different types of state: in-memory data structures vs on-disk state.
- Goal: guarantee consistency on recovery, not full persistence.
- Boundary condition reasoning: best case (complete persistence), worst case (write never persisted), and partial writes (garbage data).
- Partial or incomplete writes can cause data corruption.
- Example useful for exam understanding of crash scenarios and effect on data consistency.

**Problem statement:**
Given a timeline with a write operation to disk, followed immediately by a crash, and then a read operation, what is the expected output on the read? Consider best case, worst case, and intermediate scenarios.

**Solution:**
- Best case: data fully written and readable.
- Worst case: write did not persist; no update visible.
- Intermediate case: partial write leads to corrupted or garbage data.
- Important takeaway: without mechanisms, partial/incomplete writes can cause corruption.

_Summary: This example helps conceptualize what can happen to data in crash scenarios and sets the stage for why atomicity and consistency are critical. Be able to enumerate the space of possibilities in such a failure mode scenario, which was explicitly linked to exam-style questions._

---

### 2. Concurrent Writes to Two Files, Crash Between Writes
**Key Points**
- Writes to two different files (file descriptor 1 and 2).
- Writes can be completed out of order in persistence.
- No sequentiality guarantee without explicit controls.
- The space of possibilities of persisting subsets of blocks includes all subsets of union of mutated blocks.
- Critical insight: writes from the same process do not guarantee ordering on disk persistence.
- Emphasized that this "space of possibilities" is important and might be a freebie on the exam.

**Problem statement:**
If two writes are performed to file descriptors FD1 and FD2, both return successfully before a crash occurs, what are all the possible states of data persistence after crash? Can FD2’s data be on disk while FD1’s is not?

**Solution:**
- Best case: both writes persisted.
- Worst case: neither persisted.
- Partial persistence possible: only FD1 or only FD2 persisted.
- Due to lack of ordering guarantees, FD2 might be persisted before FD1 even if FD1 was written first logically.
- The space of possible persisted data is the power set of the union of mutated blocks from FD1 and FD2.

_Summary: This example is fundamental to understanding non-atomicity and potential reordering in file systems, which affects consistency guarantees. It also is directly linked to an exam-style reasoning problem about enumerating possibilities._

---

### 3. File Metadata and Data Separation, Update Atomicity Problem
**Key Points**
- Files consist of two main parts: metadata (stored in an inode) and actual data blocks.
- Updates must modify both data blocks and metadata pointers.
- Metadata and data updates are separate writes to different disk locations.
- Mutation involves copy-on-write of data blocks to avoid in-place mutation.
- Partial update scenarios cause inconsistency if metadata and data updates are not atomic.
- Write syscalls may return before data is persisted to disk, causing uncertainty.
- Emphasis on the non-atomicity of writes and buffering inside OS causing possible crashes with partial updates.

**Problem statement:**
When performing a write to a file, explain why updating the metadata (inode pointers) and data blocks separately can cause inconsistency in case of a crash. Why is the write system call not sufficient to guarantee data persistence?

**Solution:**
- Data blocks are copied and modified; then inode metadata is updated to point to new data blocks.
- If crash happens between data update and metadata update, the file can point to stale or corrupted blocks.
- write syscall is blocking but does not guarantee data has been flushed to disk, only that it is buffered.
- OS buffering and disk controller reorder writes, so data may not be durable yet.
- To guarantee atomicity, additional mechanisms beyond simple write calls are necessary.

_Summary: This deeper example conceptualizes the problem of metadata and data atomicity and persistence, which is a fundamental challenge in file systems. It is linked to exam questions on ordering, atomicity, and crash consistency._

---

### 4. Security Implication of Partial File Updates
**Key Points**
- Partial updates to metadata can cause files to point to blocks owned by other files.
- This breaks isolation guarantee of OS file systems.
- Potential to read data from another user's private files (e.g., SSH keys).
- Highlights an essential abstraction violation uncovered by low-level inconsistencies.

**Problem statement:**
Explain from a security perspective what can happen if during a crash the file metadata is partially updated such that a file’s inode points to data blocks belonging to another file.

**Solution:**
- The affected file can access data blocks of other files.
- This breaks file system isolation and confidentiality.
- Such leakage of data is unacceptable security-wise.
- This motivates the need for crash consistency mechanisms ensuring atomic metadata operations.

_Summary: This example ties low-level crash consistency issues to security implications, emphasizing the importance of atomicity. Worth remembering that crash consistency is critical also for isolation and security._

---

### 5. Directory Creation and File Creation Ordering Problem
**Key Points**
- Directory creation (mkdir) and file creation (open) cause related metadata updates.
- Directory blocks include directory entries (durants or dirents) that link file names to inode numbers.
- If a crash occurs such that directory metadata is synced out of order (file created before directory persisted), the file’s inode exists with no directory entry pointing to it.
- This causes inode leakage (orphaned metadata), similar to memory leaks.
- Ordering of these updates is critical.

**Problem statement:**
What could happen if the metadata corresponding to creating a directory is synced **after** the metadata for a file created inside that directory is synced? What is the concrete consequence?

**Solution:**
- The file’s inode is allocated and persisted.
- Directory entry (durant) linking file name to inode is not persisted.
- After a crash, file exists but is unreachable via the directory path.
- Leads to inode leakage and wasted disk space.
- Shows importance of ordering metadata updates during directory/file creation.

_Summary: This example illustrates metadata update ordering problems in directories, again highlighting system correctness issues relevant for exam conceptual questions on crash consistency and ordering._

---

### 6. Imposing Ordering on Disk Writes via Flush
**Key Points**
- Low-level disk interface offers only read/write single block primitives.
- No inherent guarantees on order of writes or atomicity.
- Flush operation waits until all buffered writes are persisted to disk.
- Flush can impose a "happens-before" partial order between groups of writes.
- Number of possible write orderings without ordering constraints is factorial in number of writes.
- Flush reduces possible permutations, improving predictability.
- The professor provided a mathematical example of permutations of three writes versus flush-synced writes.

**Problem statement:**
Given multiple writes to different disk blocks, describe how the flush operation can impose partial ordering and reduce the number of possible persistence orders. How many permutations exist for writes within a flush?

**Solution:**
- Without flush: all writes can be reordered arbitrarily; total permutations = (N+K)!.
- With flush separating sets of writes: permutations are N! * K!.
- For example, 3 writes in first set (3!) and 1 write in second set (1!), total 6 possible orders vs 24 without.
- Flush provides a way to impose happens-before and partial order.

_Summary: Understanding how flush affects write ordering and atomicity underpins file system correctness designs. This mathematical reasoning was explicitly noted as exam-relevant._

---

### 7. Shadowing Mechanism for Atomic Updates
**Key Points**
- Shadowing maintains two copies of data: active and shadow.
- Updates are done on the shadow copy by copying and modifying new blocks.
- After update, a single Boolean shadow bit is atomically flipped to switch active copy.
- Atomicity guaranteed by the binary nature of shadow bit (only 0 or 1 possible, no intermediate states).
- Crash during copy or update does not affect current active data.
- Crash during bit flip is atomic because it's a single bit flip.
- Ensures crash consistency by leveraging atomic flag switching.
- Performance costs: doubles space usage due to two copies.
- Requires flush operations to ensure ordering: copy/update then flush then bit flip.

**Problem statement:**
Explain how the shadowing mechanism ensures atomicity and crash consistency using a Boolean shadow bit. What are the major steps and required ordering?

**Solution:**
- Step 1: Copy current data to shadow block (copy-on-write).
- Step 2: Update shadow copy with new data.
- Step 3: Flush writes to disk to ensure copy and update finish.
- Step 4: Atomically flip Boolean shadow bit to switch active copy.
- Atomicity comes from flip being a single bit change (no intermediate states).
- Crash during copy or update: shadow bit still points to old consistent copy.
- Crash during flip: flip is atomic.
- Hence data always consistent after recovery.
- Flushing needed to enforce write ordering (copy & update complete before flipping).

_Summary: This concrete example of shadowing is fundamental and exam-relevant. Be able to describe why atomic flipping of a shadow bit yields consistency and discuss the performance tradeoffs (2X space, extra writes and flushes)._

---

### 8. Multiple Updates with Shadowing, Need for Flush between Updates
**Key Points**
- Multiple updates require shadows for each data block.
- Flush needed between updates to ensure ordering and correct shadow state.
- If subsequent update uses stale shadow, its consistency breaks.
- Flush operations create partial ordering between update sets.
- The correctness depends on ordering enforced by flushes preventing copying stale data.
- Flushes are very expensive and reduce performance.

**Problem statement:**
If performing two back-to-back updates with shadowing, do we need to flush between the bit flip of the first update and the copy of the second update?

**Solution:**
- Yes, flush is needed between the shadow bit flip of first update and copy of the second.
- Without flush, second copy could copy stale (old) data because first update's shadow bit flip not persisted.
- Flush enforces happens-before between these operations.
- Ensures subsequent updates base their copy on latest consistent data.
- Flushes degrade performance but required for correctness.

_Summary: This problem emphasizes the role of flush in maintaining ordering between shadowed updates. Important takeaway that shadowing correctness requires careful and costly coordination._

---

### 9. Professor’s Exam Emphasis and Conceptual Framework
**Key Points**
- Professor frequently framed questions as exam-style, e.g., "If I were to ask you this on the exam..."
- Fundamental concepts: crash consistency, atomicity, ordering.
- Conceptual approaches from first principles: state types, block-level updates, partial orderings.
- Explicit callouts to boundary condition reasoning & set theory for describing persistence states.
- Concrete low-level examples (inode, directory entries, shadow bit) linked to system abstractions (ordering, atomicity, isolation).
- Mathematical count of permutations for write orderings with/without flush.
- Overhead tradeoffs (shadowing doubles disk space used, flush cost).
- Preview of next lecture on logging/journaling as real-world solution.

_Summary: Attentive learners should extract these exam-like reasoning questions and be able to solve them themselves. The lecture sharpens understanding by building from fundamentals and illustrating with detailed examples._

---

# Final notes:
Be sure to practice:
- Describing the space of persistent states after crashes for single and concurrent writes.
- Explaining why writes are not guaranteed atomic or ordered at disk level.
- Reasoning about metadata and data update separation.
- Explaining the shadowing mechanism steps & atomic bit flip reasoning.
- Describing how flush imposes partial order and its cost.
- Recognizing implications on security and abstraction violations.
- Understanding inode/directory metadata update ordering issues.

These represent the core exam-relevant material according to the professor’s explicit and implicit cues in the lecture.