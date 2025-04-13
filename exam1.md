Problem 1 [Estimated Effort: 30min]

Your lab partner is an architect. He designed an 8-bit micro-architecture for his toy thermostat device, which natively supports two types of pages: a 4B “normal” page and an 8B “largepage.” He’s now trying to decide what kind of paging system to use. He knows from CS2200 that for 32-bit architecture, a two level paging system seemed like a good idea. We will define the memory overhead of a given paging system as the total bytes used by all the page table pages (including pgdir) divided by the total bytes of virtual memory allocated to (used by) a process. We expect this micro-architecture to be used for very small (micro?) processes that use only 16B for code, 16B for data, and 8B for stack. Unlike xv6, we will assume that stack is allocated from the top of the user process virtual address space.

1A. Describe the two level paging system you could implement for this 8-bit architecture using ONLY the normal and large sized pages supported. Hint: there are only three possible ways to do this. In each of the questions below, describe each one of these three uniquely different ways of partitioning your linear address and derive the memory overhead of the resulting 2-level paging system, given this linear address breakdown.

1A(i): Use this space to describe exactly how to partition 8 bits, then derive and calculate the memory overhead of the resulting 2-level paging system as defined.

1A(ii): Use this space to describe a different way of partitioning 8 bits, then derive and calculate the memory overhead of the resulting 2-level paging system as defined.

1A(iii): Use this space to describe one more unique way of partitioning 8 bits, then derive and calculate the memory overhead of the resulting 2-level paging system as defined.

1A(iv): Which of the above designs yields the most memory efficient design? Elaborate on WHY this design ended up being the most efficient, concretely referring to the implications of how many bits you allocate to (a) pgdir, (b) page table, and (c) offset.

1B: CS3210 then taught us that a 2-level paging system is not the only way to design a page table system. How would you design a 1-level paging system? Assume we no longer care about natively supported normal and largepage sizes, i.e. page table sizes and physical frame sizes can be arbitrary powers of 2.

1C: Per the definition of the memory overhead, it is clearly beneficial to reduce memory allocated to the pgdir in the 1-level paging system, as it will yield better overhead. But this creates an interesting tradeoff. Please answer the following questions.

1C(ii): What, if anything, starts to suffer (as we start reducing the number of bits allocated to pgdir for this 1-level paging system)? Clearly state ONE disadvantage or cost you have to pay for reducing the size of pgdir. If more than one disadvantage is stated, we will only grade the first one.

Problem 2: Microkernels & Scheduling [Estimated Effort: 15min]

You’re not happy with the monolithic kernel design of BuzzOS, so you decided to create your own microkernel clone of BuzzOS, calling it uBuzz. In your microkernel, you have factored out two types of services to user space: memory allocation (MS) and file services (FS), which always run. These services are not compute intensive. They handle requests to allocate memory or file system requests. Your ML training application (A) running on uBuzz IS computationally intensive, however, and is comprised of many compute intensive processes. The application cares about completing training as fast as possible.  Assume the number of processes to be >> number of CPUs in the system. You are tasked to write a scheduler for uBuzz. To reiterate, the scheduler is responsible for scheduling ALL user space processes.

2A(i) Please name two concrete success metrics that would be most pertinent to this specific scenario to evaluate the performance of this scheduler. Hint: Please note that success metrics must be quantifiable/measurable.

2A(ii) Would you use a preemptive or non-preemptive scheduler? Please justify, referring to the success metrics above.

2A(iii) Would you use FIFO policy? Please justify, referring to one or more success metrics above.

2A(iv) Would you use Round Robin for this system? Please Justify, referring to one or more success metrics.

2B. You are a CREATE-X cofounder, trying to commercialize uBuzz. You hired an intern (a recent CS3210 graduate) who factors out the Networking Service (NS) out of the core kernel as a separate user-space daemon (NS). Now, the only user space process A depends on is NS. But your kernel drops packets if they’re not processed within 10ms. How would you have to change your scheduler for this microkernel?

2C. The new NS is running well. You’re feeling good about your application A. But the second intern you hired pushed some features that make NS dependent on MS and FS internally. Explain what specific key desired property/advantage of microkernels is affected by the second intern.

2D(i). Capture the dependency graph G = {V,E}. You’re given the vertices of the graph as V = {A, MS, FS, NS, and K} (K is the kernel core). Enumerate ALL edges of this graph, i.e. give me the set E of all edges in this graph G before the second intern.

2D(ii). What edges were added by the second intern? Please specify new edges added to E.

2E. Based on the definition of the graph above, what is the failure closure of A before and after your second intern? Specify using same vertices as before.

2F. Based solely on failure isolation of application A, has it improved, stayed the same, or got worse in uBuzz compared to the monolithic buzzOS you started with? Was the complexity of uBuzz justified? Justify your answer.