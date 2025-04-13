Below is an exam that synthesizes many of the topics and “exam‐style” questions highlighted in the lecture notes. You are expected to answer these questions “from first principles” – explain your reasoning clearly and include any necessary computations or diagrams. Good luck!

────────────────────────────
Problem 1: Kernel Abstractions and Subsystem Functionality [20 min]

a) List three examples of core kernel subsystems that provide fundamental abstractions such as naming, isolation, multiplexing, and protection. For each subsystem, briefly explain one concrete functionality it supplies. 

b) Explain why the design of these subsystems (for example, networking, virtual memory management, and file systems) is critical for isolating failures and ensuring that a fault in one component does not bring down the whole system.

────────────────────────────
Problem 2: Ethernet, the OSI Stack, and TCP Reliability [25 min]

a) Describe the structure of an Ethernet header. Include the field names, sizes, and total number of bytes.

b) List the seven OSI layers (or the mnemonic given in the lecture) and explain briefly which layer is primarily responsible for IP, TCP/UDP, and Ethernet functionality.

c) Explain how TCP ensures reliable, ordered delivery over an unreliable network. In your answer, describe the roles of sequence numbers, acknowledgments, and timeouts.

────────────────────────────
Problem 3: Journaling, Ordering, and Crash Consistency [30 min]

a) In journaling file systems, explain why it is essential to enforce an ordering between data writes and metadata (or commit) records. Describe the “flush” mechanism used to ensure a “happens‐before” relationship between a log entry and its commit.

b) Consider a file update that writes three data blocks, updates the free–block list, and later updates the inode metadata. Describe what might happen if the disk crashes after the inode update is visible but before the data blocks have been safely written. How does ordered journaling prevent such inconsistencies?

c) Some systems use a “shadow bit” mechanism for atomic updates. Explain the three–step process (copy, update, atomic bit flip) in a shadowing scheme and discuss how it guarantees that a reader sees either the old or the new version but never a partially updated state.

────────────────────────────
Problem 4: Virtual Memory and Paging Calculations [35 min]

a) Explain the working of a two–level paging system. How many memory accesses (reads) does a hardware page table walk typically require to translate a virtual address? Justify your answer.

b) For a 32–bit system using two–level paging with a 10–10–12 split (10 bits for the page directory index, 10 bits for the page table index, and 12 bits for the offset), calculate:
  – The number of entries in the page directory.
  – The size (in bytes) of the page directory if each entry is 4 bytes.

c) The professor discussed an alternative “one–level” scheme for small architectures (for example, an 8–bit micro–architecture supporting two page sizes). Briefly describe one approach for partitioning a linear 8–bit address into page directory, page table, and offset fields (if applicable) and discuss how the overhead of the page tables might be calculated. (You do not need to perform exact calculations but indicate what factors affect overhead.)

d) Explain why larger pages (e.g., 4 MB) give a higher TLB coverage than smaller pages (e.g., 4 KB) and discuss the impact on TLB miss rates.

────────────────────────────
Problem 5: Concurrency, Interrupts and Spinlocks [30 min]

a) In a kernel, why is it problematic if an interrupt occurs while a regular kernel code that holds a spinlock is executing? Explain the deadlock that may ensue and what design change (hint: interrupt disable) is needed to avoid it.

b) Describe how an atomic exchange operation is used to build a spinlock. Draw (or list) the finite state automaton for the spinlock operation showing the “successful” state when the lock is acquired and the state when the thread continues to spin.

c) Consider two threads executing concurrently on a multiprocessor. If Thread 1 writes to variable X then reads variable Y, and Thread 2 writes to Y then reads X, list all possible outcome pairs for the read values (assuming initial values are 0) under a memory model that allows store-to-load reordering. Explain briefly how reordering can produce an outcome where both threads read 0.

────────────────────────────
Problem 6: Scheduling Design and Performance Trade-Offs [30 min]

a) Define two concrete success metrics (in measurable terms) that are appropriate for evaluating a scheduler in a system supporting both compute–intensive applications and low–compute background services (like memory or file services). Explain why these metrics are important.

b) Compare preemptive and non–preemptive scheduling. Under the success metrics defined in part (a), justify which approach would be more suitable for a highly loaded, compute–intensive system.

c) Round Robin (RR) scheduling is often cited as “fair” but has disadvantages. Explain one drawback of using RR in terms of tail latency or response time, and illustrate how a policy such as Shortest Remaining Time First (SRTF) might improve that aspect. Be sure to discuss the potential trade–offs, including context switch overhead.

d) Suppose you have a microkernel OS that runs most of the basic services (file, networking, memory) in user space—and one critical network service processes packets within 10 ms. Later, however, that network service itself depends on other user space services. Identify which key microkernel property is compromised by this added dependency and discuss its potential impact on system failure isolation.

────────────────────────────
Problem 7: Process Creation and Copy-on-Write [35 min]

a) Describe the traditional fork operation in systems like XV6. Explain why a “naïve” fork that copies all physical frames has a complexity O(N) (with N = number of physical frames) and why “copy on write” (CoW) reduces this cost to O(1) in the common case.

b) In a CoW system, explain what happens when the child process subsequently writes to a shared page. Include in your answer what triggers a trap, how a new physical frame is allocated, how the page table entry is updated, and why the write–permission bit is initially cleared.

c) It is sometimes useful to consider the “graph of mappings” between virtual pages and physical frames with reference counts. Explain how the operating system uses reference counting to decide whether a write on a shared frame should trigger a CoW event.

d) Discuss one challenge related to TLB invalidation when a CoW copy is performed. How many TLB invalidates are necessary and why?

────────────────────────────
Problem 8: Microkernel vs. Monolithic Kernel Designs and Inter–Process Dependency [25 min]

a) Compare and contrast microkernel and monolithic kernel architectures in terms of performance overhead and isolation benefits. In your answer, discuss the cost of context switches and TLB flushes when many services run in user space in a microkernel design.

b) A dependency graph for a microkernel system includes vertices for processes A (application), MS (memory service), FS (file service), NS (networking service), and K (kernel core).  
  (i) Before any extra dependencies are added, sketch the dependency graph (list all edges) showing the typical dependencies.  
  (ii) Now suppose a new intern makes the networking service depend on MS and FS. Explain what additional edges are added, and discuss how these extra dependencies affect the “failure closure” of application A.

────────────────────────────
Problem 9: Security and Memory Safety [20 min]

a) Consider the classic buffer overflow vulnerability. Describe what happens when a function that copies a user–provided string into a fixed–size buffer does not check for input length. Explain how an attacker might use this to hijack control flow.

b) Explain why storing only a hash of a password (even when salted) is preferable to storing plain–text passwords. Include in your answer a brief discussion on rainbow tables and why a salt, even if stored in the clear, helps mitigate pre–computed dictionary attacks.

c) Kerckhoffs’s Principle is a fundamental rule in secure system design. State this principle and explain why “security by obscurity” is not considered a robust security strategy.

────────────────────────────
Problem 10: Scheduling Under Latency Constraints and Trade-Offs [20 min]

a) Many modern schedulers must meet hard Service-Level Objectives (SLOs) for latency. In a system serving online ad requests or language model inference, explain how tail latency (for example, the 99th percentile) might be more critical than average response time. 

b) Briefly discuss the “power of two choices” algorithm in the context of load balancing. What are its advantages in terms of decision time complexity and fairness?

c) Explain why a scheduler might deliberately delay scheduling decisions (“lazy scheduling”) for a brief period. What are the benefits and what are the risks of this approach?

────────────────────────────
End of Exam

Please show all work where applicable and provide clear explanations wherever asked. Good luck!