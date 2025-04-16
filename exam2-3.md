### Question 1  
An OS designer is considering whether to implement a microkernel architecture or stick with a monolithic kernel for a new secure operating system. The design targets a multi-CPU system and must balance performance and fault isolation.

1. Describe the fundamental cost imposed on microkernels compared to monolithic kernels, explaining why this cost occurs in terms of CPU context and TLB behavior.  
2. Explain the main fault isolation advantage that microkernels provide, using the concept of failure closure and the adjacency matrix representation of system components.  
3. Give one concrete scenario or type of system workload where a microkernel might be preferable over a monolithic kernel, and one scenario where a monolithic kernel might be advantageous. Justify your choices.

---

### Question 2  
Consider a simplified 32-bit system that uses paging for memory management. The system currently uses 4KB pages (12 bits for offset) and 32-bit virtual addresses. You are now proposed to switch to an architecture with extremely small pages of 32 bytes (5 bits offset), keeping the virtual address size at 32 bits.

1. Calculate and compare the memory overhead of page tables in both architectures, expressing overhead as the ratio of PTE size over page size. Assume a page table entry takes 4 bytes.  
2. Discuss the tradeoffs of using such tiny pages compared to traditional 4KB pages, focusing on memory overhead, page table complexity, and suitability for typical process workloads.  
3. Explain why, given the address size and page size constraints, it may be impossible to support a full set of six permission bits (e.g., present, writable, user/supervisor, cache-disable, accessed, dirty) in a page table entry.

---

### Question 3  
You have a multi-level paging system with 4-level page tables typical of x86-64, which uses 48 bits of virtual addresses. Each page table page holds 512 entries (9 bits). The system supports TLB caching to speed up VA to PA translations.

1. Explain how the 48-bit virtual address is broken down among the 4 page table indices and page offset.  
2. Describe how many memory operations are needed to perform a complete two-level page table walk in a 32-bit system versus a four-level page table walk in x86-64.  
3. Discuss the role of the TLB in this multi-level paging system and explain how page size choices (e.g., 4KB small pages vs 4MB large pages) affect TLB efficiency.

---

### Question 4  
In a copy-on-write (COW) fork implementation, a child process inherits the parent's virtual address space but shares the same physical frames. Copying occurs only when a write is attempted.

1. Explain why copying the entire virtual address space during fork is unnecessary, considering memory usage and performance.  
2. Describe how the copy-on-write mechanism tracks sharing of physical pages and decides when to actually copy a page. Include an explanation of reference counting in your answer.  
3. When a process writes to a shared page, explain the backpropagation of copying required in page tables and page directories. Why might this cause multiple levels of the paging structures to be copied?  
4. Differentiate between logical permissions and physical permissions during COW, and explain why physical write bits in page tables are manipulated to implement COW.

---

### Question 5  
A system uses a two-level paging scheme with 10 bits for the page directory index, 10 bits for the page table index, and 12 bits for the offset within a 4KB page. Consider three different ways to split the 8-bit linear address space of a toy 8-bit architecture into two-level page tables supporting normal (4B) and large (8B) pages:

- (i) 4 bits PGdir + 4 bits PT + 0 bits offset  
- (ii) 3 bits PGdir + 5 bits PT + 0 bits offset  
- (iii) 5 bits PGdir + 3 bits PT + 0 bits offset  

1. For each of the above partitions, describe the size and number of entries of page directory and page tables.  
2. Calculate the memory overhead for each design, defined as total page table memory divided by virtual memory allocated.  
3. Identify which design provides the most memory-efficient paging structure for small processes, and justify your answer referring to bits allocated to directories, tables, and offsets.

---

### Question 6  
You are to design a scheduler for a microkernel-based system running a computationally intensive ML training application (many compute-heavy processes) and several lightweight always-running user-space services (memory allocator, filesystem):

1. Define two quantitative success metrics appropriate for evaluating the scheduler’s performance considering the workload characteristics.  
2. Would you prefer a preemptive or non-preemptive scheduler here? Defend your answer regarding the defined success metrics.  
3. Would a simple FIFO scheduling policy suffice? Justify your answer in terms of throughput, latency, and fairness.  
4. Would a Round Robin scheduler be beneficial or detrimental in this setup? Explain your reasoning relevant to the workload.

---

### Question 7  
Consider the interrupt handling mechanism in an x86 system:

1. Describe the sequence of actions the CPU performs from the moment an interrupt occurs in user space to the start of the interrupt handler execution in kernel space. Stress the privilege checks and stack switching involved.  
2. Explain why disabling interrupts during critical sections in kernel code that accesses shared variables is necessary to prevent deadlocks involving interrupts and spinlocks.  
3. Provide an example scenario demonstrating how a deadlock can arise if interrupts are not disabled correctly around spinlock acquisition in the kernel.

---

### Question 8  
Consider the classic “too much milk” concurrency problem with two roommates who want to buy milk if none is present.

1. Why does the naive solution where both check the fridge before buying milk lead to safety violation? Formally state which concurrency property is violated.  
2. Why is leaving a note insufficient to solve the problem? What concurrency primitives or atomic operations are needed instead?  
3. Briefly describe how hardware atomic instructions like atomic exchange can be used to implement a spinlock that guarantees mutual exclusion among threads.

---

### Question 9  
Two threads share variables X and Y, initialized to zero.

- Thread 1: `X = 1; r1 = Y;`  
- Thread 2: `Y = 1; r2 = X;`  

Assuming an x86 processor with total store order (TSO) memory model:

1. Enumerate the possible values of `(r1, r2)` after both threads execute concurrently, and explain why all observed results are possible.  
2. Explain how instruction reordering and weak memory models give rise to surprising outcomes in concurrent programs.  
3. What programming techniques or synchronization primitives can be used to enforce sequential consistency and avoid these reorderings?

---

### Question 10  
You are to implement a producer-consumer queue with multiple consumers and producers using locks and condition variables.

1. Explain why it is critical to check conditions for waiting inside a `while` loop instead of an `if` statement, citing the problem of spurious wakeups or race conditions with multiple consumers.  
2. Discuss the importance of signaling placement: what happens if `signal()` or `broadcast()` is called before the producer actually pushes a new item into the queue?  
3. Elaborate on the “happens-before” relation established by the sequence of push, signal, wait, and pop operations in the producer-consumer problem.

---

### Question 11  
A file system uses shadowing (copy-on-write) for crash consistency by maintaining two copies of the metadata and flipping an atomic shadow bit to switch versions:

1. Describe step-by-step how shadowing works to ensure atomic updates and how crash consistency is preserved, noting the role of atomic bit flips.  
2. What ordering guarantees involving disk flushes are required between copying data, updating shadow copies, and flipping the shadow bit? Why are these flushes essential?  
3. Describe the main performance cost of shadowing and explain how it impacts typical file system workloads.

---

### Question 12  
Logging (journaling) is a common mechanism to ensure file system crash consistency.

1. Explain the “supremacy clause” with respect to reading data blocks when committed log entries exist. When should the system read from the log versus from the data blocks on disk?  
2. Discuss how the happens-before relation is maintained between log entries and commits, especially focusing on the required placement of `flush` operations for atomicity and ordering.  
3. Compare two commit mechanisms: (a) sequential entry + commit writes with flushes, and (b) commit by writing a checksum for group commits. What advantages do checksums provide?  
4. What does the log merge operation entail, and how does the system ensure crash consistency during the merge process?

---

### Question 13  
Consider an ordered journaling file system.

1. Describe how ordered journaling enforces atomicity and ordering between data block writes, metadata logging, and commit records without logging data blocks. Include the sequence of operations and why this ordering matters.  
2. Discuss the performance trade-offs compared with full journaling and no journaling approaches, focusing on write amplification, latency, and possible head-of-line blocking.  
3. How does an `fsync()` on one file affect logs including unrelated files? Explain the implications on latency and performance.

---

### Question 14  
You want to implement an atomic file update purely using POSIX system calls (read, write, fsync, unlink, etc.) from user space, without relying on kernel atomicity guarantees.

1. Write a high-level pseudocode sequence of operations to implement atomic write using a temporary log file or journal.  
2. Explain why multiple calls to `fsync()` on both the log file and the directory are necessary to ensure durability and ordering.  
3. Discuss performance and complexity costs of this approach and why it is still commonly used despite overhead.

---

### Question 15  
A system uses the Clock page replacement algorithm but hardware provides only a single "present" bit for pages, without separate accessed or dirty bits.

1. Propose a software mechanism to emulate the accessed bit behavior necessary for the Clock algorithm using only the present bit and trap handling.  
2. Explain how the trap handler manages page accesses and how accessed bits are simulated.  
3. Discuss the impact on efficiency and correctness of the Clock algorithm due to this hardware limitation. What additional assumptions must the operating system make?

---

### Question 16  
You have a singleton initialization function implemented with a double-checked locking pattern that checks the singleton pointer before acquiring a lock.

1. Analyze why this implementation violates the Data Race Free 0 (DRF0) guarantee.  
2. Explain why compiler and CPU instruction reordering exacerbate this bug in multi-threaded environments.  
3. Propose a corrected implementation and reasoning that ensures safe initialization without data races.

---

### Question 17  
Given a scheduling scenario with multiple long-running jobs and many short-running jobs competing for CPU time:

1. Discuss the suitability of Round Robin for long-running jobs and explain its advantages and limitations.  
2. Compare to Shortest Job First (SJF) and Shortest Remaining Time (SRT) policies in handling short-running jobs. When is preemption necessary?  
3. Describe the trade-offs between preemptive and non-preemptive scheduling in the context of overhead and responsiveness.

---

### Question 18  
Explain why interrupt-driven I/O is preferred over polling in general-purpose operating systems.

1. Describe the disadvantages of a polling-based keyboard driver in terms of CPU utilization and latency.  
2. Explain how hardware and software interrupts improve efficiency and responsiveness.  
3. Discuss the role of the Interrupt Descriptor Table (IDT) and privilege levels in providing secure and correct interrupt handling.

---

### Question 19  
You are tasked with designing a user-space threading library:

1. Explain why user-level context switches (thread switching) can be implemented without privileged instructions.  
2. Discuss the assumptions and limitations of cooperative threading versus preemptive threading.  
3. Describe how user-space scheduling interacts with kernel scheduling in many-to-one and hybrid threading models.

---

### Question 20  
You want to understand the maximum supported file size in a file system with inodes containing 12 direct pointers and 1 indirect pointer block, each block 512 bytes.

1. Calculate the maximum file size supported by such an inode.

2. Explain why indirect pointers are needed in inodes and how they scale file size beyond that supported by direct pointers alone.

3. Describe how directory entries (durents) relate to inodes and how file lookup proceeds using inode tables and directory traversals.

---

These questions are designed to challenge students to synthesize understanding of complex OS design trade-offs, mechanisms, and conceptual foundations across isolation, paging, concurrency, scheduling, threading, file systems, security, atomicity, and networking, reflecting the lecture content and professor’s exam hints.