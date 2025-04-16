### 1. Waiting and Ordering Concurrency Code Example with Race Conditions  
**Key Points**  
- Identify shared resources in concurrent code (struct list).  
- Problem: race condition at line 15 due to concurrent insertions.  
- Interleavings cause unpredictable order, possibly corrupted data structures.  
- Solution: impose partial order using acquire-release semantics around critical section.  
- Use of locks (mutex/spin locks) to ensure atomicity in critical sections, reducing interleavings and ensuring correctness.  
- Spin lock wastes CPU cycles; conditional variables are better by blocking threads instead of busy waiting.  

**Problem statement:**  
Given concurrent code inserting elements to a linked list, what is the problem with this code? Which line is problematic? How can we fix it?  

**Solution:**  
- Line 15 is problematic because concurrent threads can interleave causing race conditions when inserting nodes.  
- Fix: protect `L1->next = list; list = L1->next;` with a lock (mutex or spinlock).  
- Use acquire-release semantics to impose partial order and ensure atomic updates.  
- Conditional variables allow threads to block instead of busy waiting, improving efficiency.  

_Summary: The professor emphasized spotting data races and non-atomic critical sections, and said this is a fundamental concept that could appear on the exam ("If I were to ask you this on the exam...")._

---

### 2. Producer-Consumer Queue with Conditional Variables and Spurious Wakeups  
**Key Points**  
- Conditional variables avoid busy-waiting in producer-consumer problem.  
- Must use a `while` loop, not `if`, to check condition before proceeding, to handle spurious wakeups and race conditions.  
- Multiple consumers waking up can cause panic if queue is empty.  
- Explanation of how spurious wakeups cause consumers to be erroneously awakened and pop empty queue.  
- Importance of atomicity in `wait` and wakeup, and checking condition again after waking.  

**Problem statement:**  
Given code of producer-consumer queue using conditional variables with `if` condition, what are the problems? Why should it be changed to a `while` loop?  

**Solution:**  
- Problem: spurious wakeups or multiple consumers waking cause attempts to pop from empty queue → kernel panic.  
- Fix: replace `if` with `while` so condition is re-checked after waking to ensure queue is non-empty before popping.  
- Even if spurious wakeups disabled, there is a race between multiple consumers that requires rechecking in `while`.  

_Summary: This specific producer-consumer example and the rationale for `while` loop (not `if`) was emphasized as an exam-worthy question ("If I were to ask you this on the exam..."), and is a fundamental concurrency concept._

---

### 3. Correct Placement of Signal Relative to Push in Producer-Consumer Problem  
**Key Points**  
- Signal must happen after push to ensure happens-before relationship.  
- Signal before push causes consumer to wake up without produce item ready → race condition.  
- Signal and wait primitives are ordered; to create partial order between push and pop, push must precede signal, signal precedes wait, and then pop.  
- Analogy with ordered journaling in filesystems: partial order enables optimizations without total order overhead.  

**Problem statement:**  
Consider different placements of `signal` relative to `push` in the critical section of producer-consumer queue. Which placements are correct or incorrect? Why?  

**Solution:**  
- Signal after push works correctly because push happens before signal; consumers wake after item is pushed.  
- Signal before push fails because wakeup happens before item is ready.  
- The happens-before relationship: push → signal → wait → pop ensures correctness.  
- Similar to ordered journaling in file systems where partial order enables correctness and optimization.  

_Summary: This example draws a conceptual parallel between concurrency synchronization and file system journaling. It was explicitly called a "practice exam question" and marked as very important._

---

### 4. User vs Kernel Threads: Advantages and Disadvantages  
**Key Points:**  
- Kernel threading: One-to-one mapping; true concurrency on multiprocessors; overhead in maintaining many kernel threads; pre-emption allows scheduling out blocked threads.  
- User threading: Many user threads to one kernel thread; low overhead; problem is blocking in one user thread stalls all; no true concurrency on multiprocessors.  
- Hybrid threading (many-to-many): compromises between the two, reduces context switches, allows some concurrency.  
- Important exam question: Explain advantages and disadvantages of each model.  

**Problem statement:**  
Describe the trade-offs between kernel threads, user threads, and hybrid threading models. What are the primary advantages and disadvantages?  

**Solution:**  
- Kernel threads: true parallelism, preemption, but overhead in creation and maintenance.  
- User threads: lightweight, efficient, but blocking stalls process; no parallelism on multicore.  
- Hybrid: partial concurrency, fewer context switches, but some blocking can still stall kernel threads.  
- Kernel threads provide better fine-grained control to kernel scheduler.  

_Summary: The professor explicitly said these advantages and disadvantages are important and hinted at exam relevance ("If I were to ask you for them on the exam...")._

---

### 5. Filesystem I-node Size Calculation with Direct and Indirect Pointers  
**Key Points:**  
- I-node structure: 12 direct pointers + 1 indirect pointer block of 128 pointers.  
- Largest file size calculation by summing the number of blocks addressable times block size.  
- Direct pointers address 12 blocks; indirect pointer block addresses 128 blocks.  
- Calculate total maximum file size from these.  
- Practice exam problem: Given inode structure, calculate largest file size.  

**Problem statement:**  
For an inode with 12 direct pointers and 1 indirect pointer pointing to block with 128 direct pointers, with each block size 512 bytes, what is the largest file size supported?  

**Solution:**  
- 12 direct blocks * 512 B = 6 KB  
- 128 indirect blocks * 512 B = 64 KB  
- Total = 70 KB largest file size supported.  

_Summary: The professor explicitly said you should be able to answer max file size from inode structure and carefully count blocks and sizes. This is a concrete example akin to examples in labs and likely exam question._

---

### 6. Opening File via Directory I-nodes and Directory Entries  
**Key Points:**  
- Directories are special files containing directory entries (durents) with inode number and name.  
- Directory inode points to data blocks holding durents.  
- To open file by absolute path, file system accesses i-nodes in order along the path.  
- Practice exam question: Given path and inode table (mapping names to i-nodes), what is the order of i-node accesses to open the file?  

**Problem statement:**  
Given an absolute path and a table of inode numbers for directory and files, list in order which inode blocks are accessed to open the file.  

**Solution:**  
- Access root inode (0), then subdirectory inode (1), then file inode (2), and so forth following the path components.  

_Summary: This example tests understanding of directory structures and file lookups, a fundamental file system concept. The professor expects students to be able to trace the inode lookups along a path._

---

### 7. File System Logging and Crash Consistency: Prefix Property and Checksum  
**Key Points:**  
- Log entries are written sequentially with prefix property: only entries up to first invalid entry are considered committed.  
- Uncommitted entries are ignored during recovery.  
- Checksumming log entries allows writing them atomically in one operation without intermediate flushes.  
- Logging ensures ordering and atomicity in file system operations.  
- Cost: doubles writes (writing to log then data).  
- Options: no logging, ordered logging, metadata logging, full logging with trade-offs in cost and consistency guarantees.  

**Problem statement:**  
Explain how logging ensures crash consistency with the prefix property and checksums. Why is double write cost incurred? What are the trade-offs between logging modes?  

**Solution:**  
- Prefix property: only valid log prefix is considered for recovery.  
- Checksums ensure corruption is detected and allow atomic writes without extra flushes.  
- Double write cost because data is written to log first, then to actual location.  
- No logging is cheapest but unsafe; ordered logging balances safety and cost; full logging has high overhead but safest.  

_Summary: This example connects theory and practical constraints of file system design. The professor emphasized the conceptual beauty and performance tradeoffs._

---

# Summary of Exam-Relevant Examples Highlighted in Lecture Transcript  
- Code race condition example with list insertions and fixing with locks/acquire-release.  
- Producer-consumer queue with conditional variables, spurious wakeups, and use of while loop.  
- Correct signal placement relative to push for happens-before relationship in concurrency primitives.  
- User vs kernel threading models: their pros and cons, and hybrid model overview.  
- Calculating max file size from inode pointer structure (direct + indirect).  
- File lookup i-node access order from absolute path and directory structure.  
- File system logging for crash consistency, prefix property, checksums, and trade-offs of logging modes.  

All of these were emphasized as fundamental or exam pertinent by the professor with explicit hints about exam. The professor also linked many of these examples to first principles and conceptual thinking. Mastery of these will be essential for the exam.