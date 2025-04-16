### Question 1  
You are designing a paging system for a simplified 32-bit architecture with 4KB pages. Consider two options for the page table structure: (A) a single-level page table with 1 million entries (2^20), and (B) a two-level paging system dividing the 20 bits of page number into two 10-bit indices.  

1. Describe the memory overhead for each design in terms of page table size (bytes).  
2. Compare the trade-offs between them regarding memory overhead and the number of memory accesses needed per virtual-to-physical address translation.  
3. Which design would you choose for a workload with many small processes using few pages, and why?  

---

### Question 2  
In a 64-bit architecture using 4-level paging, the virtual address uses only 48 bits, split into four 9-bit indices and a 12-bit offset.  

1. Explain why only 48 bits are used out of 64, and how this affects virtual address canonical form.  
2. Calculate how many entries are in each page table level.  
3. How many memory accesses does the CPU perform in the worst case during virtual address translation (walk through all levels, no TLB hit)?  
4. Discuss the impact of TLB hits and misses on this process and why TLB is critical for performance.  

---

### Question 3  
During kernel boot, two distinct virtual pages are mapped to the same physical frame (memory aliasing). One resides at the very bottom of the virtual address space, the other at a higher offset.  

1. Explain the concept of memory aliasing in this context and its purpose during bootstrapping.  
2. Why is the low address aliasing entry deleted after boot, replaced by per-process user-space mappings?  
3. How does this aliasing impact page directory setup and system initialization correctness?  

---

### Question 4  
The present bit in page directory and page table entries is critical. Consider an OS that uses a function walkpgdir(pgdir, va, alloc) which, given a virtual address va, returns a pointer to the page table entry (PTE), optionally allocating a new page table if missing.  

1. Describe how the present bit controls the branching logic in this function.  
2. Explain the process of allocating a new page table page on-demand; what bits must be set in the PDE afterwards?  
3. What could go wrong if the present bit is not checked properly in virtual-to-physical address translation?  

---

### Question 5  
Forking a process typically copies the entire virtual memory of the parent. Copy-on-write (COW) optimizes this by initially sharing pages.  

1. Explain why copying the entire virtual address space immediately during fork is inefficient.  
2. Describe with an example what happens when a shared page is written to by the child after fork under COW.  
3. How do reference counts help the OS decide when to copy a page?  
4. What is the back-propagation effect in page table and page directory copying due to COW?  

---

### Question 6  
Describe the differences between logical permissions and physical permissions in the context of copy-on-write memory management. Specifically:  

1. What role does the page table write bit play during COW?  
2. Why does the OS temporarily disable physical write permission on pages that should be logically writable?  
3. How does the CPU trap and OS handle writes to such pages?  

---

### Question 7  
Suppose you design a two-level page table for an 8-bit virtual address space, with pages sized at either 4 bytes (“normal”) or 8 bytes (“large”). The process virtual memory is very small (16 bytes code, 16 bytes data, 8 bytes stack).  

1. Enumerate all unique ways to split the 8-bit virtual address into PGDIR index, PT index, and offset under these constraints.  
2. Calculate the memory overhead (page table size / virtual memory size) for each design.  
3. Identify which design is most memory efficient, justifying your answer with respect to bits allocated and resulting page table sizes and offsets.  

---

### Question 8  
You are implementing the clock page replacement algorithm on a system which only provides a "present" bit in page tables (no accessed or dirty bits).  

1. Propose a mechanism to record the accessed status of pages using only the present bit, trapping page faults appropriately.  
2. Explain how your mechanism allows the clock algorithm to estimate page usage effectively.  
3. Discuss performance implications and correctness guarantees compared to a system with full hardware support for accessed and dirty bits.  

---

### Question 9  
Your kernel code and interrupt handler both access a shared variable protected by the same spinlock. The interrupt handler may preempt the kernel code at any time.  

1. Explain why this arrangement can cause a deadlock.  
2. How does disabling interrupts while holding the spinlock prevent this deadlock?  
3. Discuss the concept of *relative atomicity* in this context.  

---

### Question 10  
Consider a scenario where two roommates, Alice and Bob, both try to buy milk if none is in the fridge. They each check, then decide to buy milk, possibly at the same time.  

1. What concurrency principle does this scenario violate?  
2. Why does placing a note ("I bought milk") not solve this issue if note writing and checking are separate steps?  
3. Suggest a synchronization primitive or algorithmic approach to ensure only one buys milk.  

---

### Question 11  
Explain the concept of an atomic exchange (xchg) instruction and how it can be used to implement a spinlock acquire function.  

1. Describe the state machine of lock and result variables during lock acquisition.  
2. What condition signifies successful lock acquisition?  
3. Why is xchg preferable over separate read and write instructions for lock implementation?  

---

### Question 12  
Two threads concurrently execute:  

- Thread 1: `X=1; EAX=Y;`  
- Thread 2: `Y=1; EBX=X;`  

All variables are initially zero.  

1. List all possible final values of `(EAX, EBX)` considering x86's Total Store Order memory model.  
2. Explain why these results can occur, considering instruction reordering and hardware memory model.  
3. What does this mean for the guarantee of sequential consistency in concurrent execution?  

---

### Question 13  
In a microkernel OS design, OS services like memory management and file systems run in separate user-space processes.  

1. What is the major performance cost of this design compared to a monolithic kernel?  
2. How does address space switching contribute to performance overhead during interprocess communication?  
3. What benefits does this design provide in terms of failure isolation and security?  
4. Provide an example scenario in which a microkernel’s isolation is a significant advantage.  

---

### Question 14  
Describe the trade-off between achieving perfect CPU isolation between processes and allowing an infinite number of processes.  

1. Why is perfect isolation incompatible with infinite processes?  
2. How can fixing an upper bound on the number of processes enable perfect isolation?  
3. What inefficiencies does this approach impose on CPU utilization?  

---

### Question 15  
A 32-bit system uses 32-byte pages instead of traditional 4KB pages.  

1. Compute the page table overhead (size of page table entry divided by page size).  
2. Compare the overhead to a traditional 4 KB page system.  
3. Discuss challenges and trade-offs that arise from using such small pages.  

---

### Question 16  
Explain the role of the execute (X) permission bit in page tables and how it helps prevent stack overflow attacks.  

1. What security vulnerability does marking the user stack as non-executable mitigate?  
2. Why is separating code and data segments into different pages necessary for applying the execute bit differently?  
3. How would you modify an OS like XV6 to support distinct execute permissions for code and data pages?  

---

### Question 17  
Describe the mechanism of logging (journaling) in file systems for crash consistency.  

1. Explain the "supremacy clause" in journaling.  
2. What is the purpose of commit records in the log, and how do they ensure atomicity?  
3. How does the flush operation support happens-before semantics between entries and commits?  
4. Contrast logging with shadowing in terms of performance and correctness guarantees.  

---

### Question 18  
In an ordered journaling file system, a file’s data blocks are written directly to disk, but metadata updates are journaled.  

1. Describe how ordered journaling ensures atomicity without logging data blocks.  
2. In case of a crash, how does the system decide to keep or discard data and metadata updates?  
3. Discuss the role of flushing to enforce correct ordering guarantees.  

---

### Question 19  
You have a producer-consumer queue with multiple consumers waiting on a conditional variable.  

1. Why must the waiting conditional be checked in a **while** loop rather than an **if** statement?  
2. What problems arise if spurious wakeups occur and the condition is not rechecked?  
3. Illustrate a scenario where multiple consumers cause race conditions if the condition check is done only once.  

---

### Question 20  
Explain the advantages and disadvantages of one-to-one, many-to-one, and hybrid threading models regarding concurrency, blocking behavior, and performance.  

---

### Question 21  
Given an inode with 12 direct pointers and 1 indirect pointer block containing 128 pointers, with each block size 512 bytes, calculate the maximum file size supported by this inode.  

---

### Question 22  
You want to atomically update a file in user space on a POSIX system without kernel transactional support. Propose a procedure using log files and fsync calls, and explain why multiple fsync calls (to log file, directories, etc.) are necessary for crash consistency.  

---

### Question 23  
Describe the steps occurring during a context switch in an OS kernel from one user process to another, including transitions between user space and kernel space and the role of the kernel stack.  

---

### Question 24  
You observe that after a process writes to a page it shares with another, the OS creates a new copy of that page but also must copy the corresponding page table and page directory pages.  

1. Explain why copy-on-write can cause this cascade of copies in paging structures.  
2. How does reference counting help control this behavior?  
3. Discuss the performance implications and possible optimizations.  

---

### Question 25  
You have a linked list shared by multiple threads, and insertions into the list are not protected by locks.  

1. Identify the concurrency problem and its consequences.  
2. Propose how locks with acquire-release memory semantics can fix the problem.  
3. Discuss the trade-offs between spinlocks and condition variables in this context.  

---

### Question 26  
You are implementing a Round Robin scheduler with a fixed time quantum. Consider a workload with a mixture of short and long running jobs.  

1. Describe how Round Robin handles these jobs and its impact on response time and fairness.  
2. Compare Round Robin with Shortest Remaining Time First (SRTF) scheduling for this workload.  
3. What scheduling policy would you choose for minimizing average waiting time in this scenario?  

---

### Question 27  
Describe how a Translation Lookaside Buffer (TLB) improves paging performance, and explain the impact of page size on TLB hit ratio and efficiency.  

---

### Question 28  
In a networking stack, a packet is sent from an application on Host A to Host B, traversing the OSI layers.  

1. List the headers appended at each layer from the application down to physical transmission.  
2. Explain the purpose of each header and the overhead introduced.  
3. How do these headers contribute to naming, multiplexing, and protection abstractions in networking?  

---

### Question 29  
TCP provides reliability over an unreliable network.  

1. Explain the role of sequence numbers and acknowledgments in achieving this reliability.  
2. Why are retransmission timeouts necessary?  
3. Illustrate with an example how out-of-order packets are handled by TCP.  

---

### Question 30  
You must design a scheduler for a microkernel OS where core OS services run as user processes. A computationally intensive ML training application runs many processes.  

1. What performance metrics are pertinent for evaluating your scheduler?  
2. Would you implement preemptive or non-preemptive scheduling? Justify your choice related to those metrics.  
3. How would presence of high-priority, low-computation services (memory and file systems) influence your scheduling decisions?  

---

These questions comprehensively probe OS design, virtual memory, concurrency, scheduling, IO, networking, and security concepts emphasized by the lectures. They require conceptual reasoning, system design tradeoffs, and quantitative calculations — matching the professor’s exam style and expectations.