### Question 1  
You have designed an 8-bit virtual memory system that supports only two page sizes: a 4-byte normal page and an 8-byte large page. You want to implement a two-level paging system for processes whose virtual address space fits in these 8 bits.  

**1A.** Describe three different valid ways to split the 8-bit virtual address into `[pgdir index | page table index | offset]` using only the supported page sizes, explaining the size of each component in bits for each way. For each split, calculate the memory overhead defined as:  
> overhead = (total bytes used by all page tables, including page directory) / (total bytes of virtual memory mapped)  

Explain your assumptions clearly.  

**1B.** Among the three designs in 1A, which one is the most memory-efficient? Explain why based on the bit allocation for pgdir index, page table index, and offset.  

**1C.** Suppose you decide to implement a single-level paging system instead, with arbitrary page sizes (not restricted to 4B or 8B). How would you design the page table structure? Briefly discuss the memory overhead characteristics compared to the two-level designs above.  

**1D.** If in the single-level design you reduce the size of the page directory to reduce memory overhead, what is one negative consequence regarding page table management or process behavior? Clearly state the cost you pay.

---

### Question 2  
You are implementing a microkernel OS based on the uBuzz system. The kernel factors out Memory Service (MS), File Service (FS), and Networking Service (NS) into user-space daemons, all communicating with the kernel and each other. Your ML application (A) depends on NS, which itself depends on MS and FS after second intern modifications.  

**2A.** Draw and clearly label the dependency graph \( G = \{V, E\} \) where \( V = \{A, MS, FS, NS, K\} \) and edges correspond to dependency relationships before and after the second intern's changes. List all edges before and after explicitly.  

**2B.** Explain how these dependencies affect failure isolation of application A in the microkernel design compared to a monolithic kernel. Quantify whether failure isolation has improved, remained the same, or worsened, and justify your answer.  

**2C.** Your kernel drops network packets not processed within 10ms. How should your scheduler be designed (e.g., preemptive vs non-preemptive, scheduling policies) to best support NS's performance requirements? Name at least two success metrics relevant to scheduler performance for this setting and justify your design choices in terms of these metrics.

---

### Question 3  
The x86-64 architecture uses a 4-level paging scheme to translate 48-bit virtual addresses to physical addresses. Each page is 4KB, and each page table entry (PTE) is 8 bytes.  

**3A.** Show the bit-level breakdown of the 48-bit virtual address into page map level 4 (PML4), page directory pointer table (PDPT), page directory (PD), page table (PT) indices, and offset. How many bits are allocated for each component?  

**3B.** Calculate the number of entries per page table or directory at each level. Show your work using the page size and PTE size.  

**3C.** How many memory accesses does it take to translate one virtual address to a physical address on a TLB miss (ignore TLB misses on lower tables)? Explain each step briefly.  

**3D.** Explain the role of the TLB in this process and discuss how page size choices (e.g., 4KB vs 2MB large pages) affect TLB hit rates and latency of address translation.

---

### Question 4  
In XV6, the function `walkpgdir` takes a virtual address (VA) and a page directory (PGDR), optionally allocating a page table if necessary, and returns a pointer to the page table entry (PTE) for that VA.  

**4A.** Describe in detail the steps taken by `walkpgdir` to locate the PTE for a given VA. Explain how the present bit and allocation flag affect behavior.  

**4B.** Explain why `walkpgdir` zeroes out newly allocated page tables and sets appropriate bits in the page directory entry after allocation. What would happen if it didn't?  

**4C.** Explain why the least significant 12 bits are reserved for the page offset and how those bits factor into the calculation of `PGX(VA)` and `PTX(VA)` (the page directory and page table indices).

---

### Question 5  
After a copy-on-write fork, both parent and child share the same physical pages initially, with write permissions disabled on actual hardware page tables.  

**5A.** Explain why the copy-on-write mechanism clears the physical write permission bit despite logically granting the process write access. What happens when a process tries to write to such a page?  

**5B.** Describe the sequence of copy-on-write steps that occur when the child writes to a shared stack page after fork. Include the changes required in physical frames, page tables, and page directory entries.  

**5C.** Explain why mutations to a single page may cascade and require copying page tables and directories, not just the physical pages.  

**5D.** In this scenario, how many TLB invalidations must the OS perform on a successful copy-on-write? Justify your answer.

---

### Question 6  
You are asked to implement the clock page replacement algorithm on hardware that only provides a `present` bit per page, and no `accessed` or `dirty` bits.  

**6A.** Explain how you can use the `present` bit and software mechanisms to emulate the presence of an `accessed` bit to implement the clock algorithm.  

**6B.** Why is lack of hardware `accessed` and `dirty` bits detrimental to the efficiency of the clock page replacement algorithm?  

**6C.** Describe the worst-case behavior of your clock-based page eviction under the constraints of this hardware support.

---

### Question 7  
You have two threads executing the following code concurrently:  
- Thread 1: `X = 1; EAX = Y;`  
- Thread 2: `Y = 1; EBX = X;`  

Assuming initial `X = 0`, `Y = 0`.  

**7A.** List all possible final values of `(EAX, EBX)` after both threads execute concurrently on an x86 processor with total store order (TSO) memory model.  

**7B.** Explain why the result `(EAX=0, EBX=0)` is possible despite the appearances of writes preceding reads.  

**7C.** What property must a program have to guarantee sequential consistency on x86?

---

### Question 8  
Two roommates want to avoid buying too much milk. Both check the fridge: if empty, buy milk. If not, do nothing. Both start at the same time; the fridge is empty.  

**8A.** Explain why this naive algorithm leads to both roommates buying milk (too much milk problem).  

**8B.** Which concurrency property is violated (safety or liveness)? Define the violated property.  

**8C.** Propose a concurrency control mechanism to prevent the problem and justify how it ensures safety.

---

### Question 9  
You are implementing a producer-consumer queue using locks and condition variables. Consider two consumers waiting on an empty queue. Suppose the producer signals the condition variable when pushing an item.  

**9A.** Explain why the consumer must test the queue empty condition in a **while loop** before waiting, instead of a simple `if` statement.  

**9B.** What can go wrong if the consumer uses an `if` statement? Illustrate a possible interleaving that breaks safety.  

**9C.** Explain the happens-before ordering relationship established by a proper signal/wait pair and why it guarantees consumers see pushed items after waking.

---

### Question 10  
Consider a file system inode that contains 12 direct pointers and 1 single indirect pointer, with each block size 512 bytes.  

**10A.** Calculate the maximum file size supported by this inode structure. Show your calculations.  

**10B.** The inode size is 64 bytes. Assuming the boot sector and superblock each occupy 512 bytes, compute the byte offset on disk of inode number 15.  

**10C.** Explain why matching the file system block size to the VM page size simplifies swapping and paging.

---

### Question 11  
Crash consistency scenario: You crash immediately after writing a block to disk but before the write completes fully.  

**11A.** List the possible states of the data read after reboot (assuming no journaling or logging).  

**11B.** If you perform writes to two different files before crashing, explain all the possible persistence states of these files after reboot. Could one file's data be persisted while the other's is not?  

**11C.** Explain why writes to metadata (inode) and data blocks pose special consistency challenges. What happens if a crash occurs between these writes?

---

### Question 12  
You want to implement atomic updates using shadowing: maintaining a current copy and a shadow copy of all data.  

**12A.** Explain each step of the shadow update process to ensure atomicity and crash consistency.  

**12B.** Discuss the performance overheads introduced by shadowing.  

**12C.** Why are flush operations critical between copying, updating the shadow, and flipping the shadow bit?  

**12D.** When performing multiple consecutive shadow updates, why is flushing required between updates?

---

### Question 13  
Explain how a file system journal (log) uses a **commit record** and the **supremacy clause** to ensure crash consistency.  

**13A.** When reading a block that has been written to both the data area and the log, from which do you read? Under what condition?

**13B.** Why is it necessary for the log commit records to appear as a prefix (no partial commits)?  

**13C.** Describe how commit checksums enable group commits and reduce flushes compared to commit bits.

---

### Question 14  
Describe the **log merge** process in logging file systems.  

**14A.** What happens if the system crashes during a log merge?  

**14B.** Explain how idempotency of writes helps maintain crash consistency during log merges.

**14C.** Explain how the log is atomically cleared after a merge completes.  

---

### Question 15  
Discuss the tradeoffs between **metadata-only logging (ordered journaling)** and **full logging** of both data and metadata.  

**15A.** How does ordered journaling guarantee atomicity of metadata updates without logging data?  

**15B.** Describe the impact of head-of-line blocking and log capacity in full logging when writing a large data file followed by a small metadata update.  

**15C.** How does calling `fsync` on one file affect unrelated file writes in ordered journaling systems? Why?

---

### Question 16  
Given only POSIX primitives (`read`, `write`, `fsync`, etc.), you want to ensure atomic update of a file from userspace (without relying on kernel guarantees).  

**16A.** Write pseudocode describing the process to atomically update a file using a log file and multiple `fsync` calls.    

**16B.** Explain why multiple `fsync` calls on the log file, directories, and target file are necessary.  

---

### Question 17  
You are considering modifying the XV6 guest OS so that user-space binary code pages have execute permission enabled, but user-space binary data pages have execute permission disabled.  

**17A.** What changes to the memory layout or page table setup are necessary to support different execute bits for code and data regions?  

**17B.** Explain why it is not possible to have different execute permissions if code and data reside in the same physical page.

---

### Question 18  
Discuss the tradeoffs of different threading models in operating systems: one-to-one, many-to-one (user threads), and hybrid threading.  

**18A.** List advantages and disadvantages of each model in terms of blocking behavior, kernel visibility, overhead, and parallelism.  

**18B.** Explain why user space threading libraries can implement context switches without kernel privilege.  

**18C.** Describe the concept of having a dual scheduler: one in user space managing user threads, one in kernel space managing kernel threads or processes.

---

These questions collectively demand synthesis, design reasoning, and quantitative evaluation drawn from your lecture materials up to midterm scope. Focus especially on understanding tradeoffs, atomicity/correctness concepts, and system-level abstractions rather than rote memorization.