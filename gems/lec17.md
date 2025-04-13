Below is a detailed list of every exam‐style example, complete with the explicit problem prompt (or paraphrase) and the professor’s exposition of what a “good answer” would look like. In many cases the professor even noted “if I were to ask you this on the exam” or stressed “very important” points. I’ve included the sections (with contextual time‐markers or cues from the lecture transcript) and the professor’s line‐of‐thinking so you can review and practice them yourself.

───────────────────────────── 
1. Microkernel vs. Monolithic Kernel – Costs and Benefits  
───────────────────────────── 
• Example prompt (Practice Exam, Q1):  
 “The question is asking: What are the costs of using a microkernel over a monolithic kernel? Please explain why these costs are fundamental to a microkernel.”  
 – Professor’s solution highlights that because many OS services are implemented as user‐space processes, you incur extra context switches (including TLB flushes due to changing address spaces), which introduces overhead.  
 – He also noted that although this cost may be “fairly straightforward” to answer (a microkernel has more context-switch overhead), one should be prepared to elaborate if the exam asks which overhead is less important (and possibly compare specific numbers or tradeoffs).  
  
• Hints from lecture:  
 – “if I were to ask you this on the exam” he pointed out the importance of explaining that each service now incurs a context switch and that a TLB flush occurs when switching address spaces.  
 – The professor stressed the emphasis on modularity versus raw performance.

───────────────────────────── 
2. Microkernel Isolation – Benefits Provided by Isolation  
───────────────────────────── 
• Example prompt:  
 “What benefits do we get from the isolation provided by the microkernel?”  
 – The professor answers that isolation produces better fault isolation. For example, if one user‑space service (like a disk driver) fails, it won’t bring down the entire kernel; this narrows the attack surface (invoked via the “SPARTA analogy”) and allows each component to be smaller, easier to update, and manage.  
 – He also compared that to a monolithic kernel where all processes “depend on all” components (a dense dependency adjacency matrix).  

• Hints from lecture:  
 – Professor stresses that “fault isolation” and having a “narrow attack surface” are fundamental points that could be asked on the exam.  
 – The discussion included concrete examples (for instance, file system servers running in user space versus in kernel space).

───────────────────────────── 
3. Perfect CPU Isolation and Scheduling  
───────────────────────────── 
• Example prompt (“Harry’s Question”):  
 “Harry wants to achieve perfect CPU isolation between processes so that a process cannot detect the number of other processes running based on its own CPU usage. Explain why achieving such perfect isolation conflicts with the abstraction of an infinite number of processes and describe how you might overcome this by imposing an upper bound (N) on the number of processes.”  
 – Professor’s solution:  
  ◦ In an infinitely multiplexed system the quantum of time per process goes to zero (T/N as N → ∞), so perfect isolation is impossible.  
  ◦ To solve this, one can apply admission control (only allow up to N processes) and use a round‑robin scheduler. Every process gets the same amount of CPU time regardless of the “real” number of processes; empty slots simply cause a no‑op (or sleep).  
 – This reasoning touches on the scheduling time not being a function of N (constant allotment per slot) to avoid leaking information.

• Hints from lecture:  
 – Emphasis on “if you expect sequential consistency… you should not block on waiting for context switches” and then a later discussion addressing that the scheduler must always allocate exactly the same time slice regardless of the number of processes.  
 – The professor indicated that “this is one of those typical questions” whose structure (advantages/disadvantages plus a concrete scheduling use-case) should be mastered.

───────────────────────────── 
4. 32‐Bit CPU Architecture with 32‑Byte Pages – Memory Overhead Analysis  
───────────────────────────── 
• Example prompt:  
 “A new 32‑bit CPU architecture uses a 32‑byte virtual memory page instead of the standard 4‑KB page. Would you expect the kernel running on this architecture to be more or less memory efficient than one using 4‑KB pages? Explain by quantifying the overhead involved.”  
 – Professor’s solution:  
  ◦ Start by noting that with 32‑byte pages you need 5 bits for the offset and 27 bits for the frame number.  
  ◦ With 4‑byte (32‑bit) PTEs one PTE is dedicated per physical frame, resulting in an overhead of 4/32 ≈ 12.5%.  
  ◦ By contrast, with 4‑KB pages the overhead is much lower (about 4/4096 or roughly 1/1024).  
 – He further explains that you must also account for the fact that page table pages are allocated as full pages even if only a few entries are used.

• Hints from lecture:  
 – The professor stressed “remember that number, 32 bytes, because that’s important.”  
 – He walked through a step‐by‐step breakdown of the linear address and PTE calculations, suggesting these numeric evaluations and derivations are exam candidates.

───────────────────────────── 
5. Hardware Permission Bits and Page Table Entry Limitations  
───────────────────────────── 
• Example prompt:  
 “Robert’s hardware design requires support for six permission bits (for reading, writing, user/super-user, disable hardware caching, accessed, and dirty bits). Given your design, can you support six permission bits? Explain why or why not.”  
 – Professor’s solution:  
  ◦ By analyzing the address breakdown (27 bits for the frame number and 5 lower‑level bits allocated to permission bits), there aren’t enough bits available to support six permission bits.  
 – This is a more direct application of first-principles resource counting in an architecture design.

• Hints from lecture:  
 – The professor indicated “that six is too many because we only have five permission bits available.”  
 – Emphasis was placed on always starting with the breakdown of the linear address.

───────────────────────────── 
6. User‑Space Execute Bit Protection on the Stack (X‑bit Example)  
───────────────────────────── 
• Example prompt (Q4 on the exam):  
 “What advantage may there be for marking userspace stack as non‑executable? In a scenario like a stack overflow attack, can malicious code be executed if the X bit is cleared?”  
 – Professor’s solution:  
  ◦ The answer is that a non‑executable stack prevents code execution from that area, thwarting exploits that overwrite the EIP with injected code (e.g., “malicious code” on the stack).  
 – This is a straightforward security question directly tying into the previous security lecture.

• Hints from lecture:  
 – Professor directly stated “if we went with Mike’s stack overflow example, would you be able to mount an attack if the X bit is set to zero? No.”  
 – Emphasis was placed on understanding that code and data should be separated per‐page for proper application of the execute bit.

───────────────────────────── 
7. Modifying Xv6 – Separating Code and Data Pages to Enforce X-bit Policies  
───────────────────────────── 
• Example prompt:  
 “Imagine you want to modify Xv6 so that the user binary code space has the X-bit set (executable) but the binary data space does not. What change(s) would you have to make in the exact call or runtime to achieve this separation?”  
 – Professor’s solution:  
  ◦ The key is to ensure that code and data end up on different physical frames because page-table entry (PTE) permissions are granted at page granularity.  
  ◦ He explained that since the current Xv6 often maps code and data into the same page, you must modify your allocation (or the ‘exact call’ routine) so that the code segment and data segment are allocated on separate pages, allowing you to set the execute bit only on the code page.  

• Hints from lecture:  
 – The professor said “if the code and data are in the same page, then you cannot control the permission bits separately.”  
 – He stressed that the starting point is to know where code and data are allocated in the virtual address space.

───────────────────────────── 
8. Modifying the Clock Page-Swapping Algorithm Under Limited Hardware Support  
───────────────────────────── 
• Example prompt:  
 “In an architecture that only provides a ‘present bit’ (without dedicated accessed or write permission bits), how can you efficiently track the access state for a page and implement the clock replacement algorithm?”  
 – Professor’s solution:  
  ◦ Walk through the finite state automaton for the “accessed variable” that must be maintained in software.  
  ◦ The only available bit (present bit) is used to mirror the accessed state. When a page fault occurs (or trap), the trap handler sets the accessed variable (transition from 0 to 1) and then resets the present bit accordingly.  
  ◦ This is done so that the clock algorithm (running on a trap handler) resets bits and iterates until it finds a page with an accessed variable of 0.  
 – He further explains that because there is no hardware write-tracking, the design must make a “conservative assumption” that every evicted page has been modified (dirty) and must be written to disk.

• Hints from lecture:  
 – The professor underlined “the most inefficient but most straightforward solution” and then refined it with an improved mechanism using a finite state automaton.  
 – He stressed that “this is very important to understand – the only mechanism we have is the present bit.”

───────────────────────────── 
9. Singleton Initialization Code – Concurrency and the DRF0 Guarantee  
───────────────────────────── 
• Example prompt (Q6 on the practice exam):  
 “Your friend Robin has written some clever code to make Singleton initialization more efficient (using a double‐checked locking technique). What is wrong with the code, if anything? Explain the problem and propose a fix.”  
 – Professor’s solution:  
  ◦ The code attempts to avoid locking by checking if the shared variable P (the pointer to the singleton) is NULL before acquiring the lock. However, this is unsafe because without the DRF0 (data‐race free) guarantee the compiler and hardware may reorder accesses so that the check and subsequent access are not sequentially consistent.  
  ◦ Thus, even if P appears to be non‑NULL, the object may not yet be completely constructed, leading to a race condition.  
  ◦ The fix is to eliminate the outer unsynchronized check or otherwise enforce stricter memory ordering (i.e. use proper locking so that all accesses to P are ordered).  

• Hints from lecture:  
 – The professor walked through the code line by line, identifying the “critical shared variable” and the problem that it might be accessed out of order because of compiler or hardware reordering.  
 – He emphasized “DRF0” and mentioned that “if you don’t have DRF0, all bets are off.” He also explained that the “clever” (but dangerous) assumption of sequential consistency is what breaks the code.  

───────────────────────────── 
Final Notes for Studying:  
• Notice how in each case the professor not only gave the problem prompt but also stressed which parts of the answer are “very important or fundamental,” and even noted when an exam question might further probe trade‑offs.  
• Be sure to be comfortable with:  
 – Deriving overhead ratios (e.g. 4 bytes per 32-byte page)  
 – Calculating the breakdown of bits in a linear address  
 – Reasoning through finite state automata for limited hardware support cases  
 – Explaining why certain locking or scheduling patterns work or break  
 – Discussing the trade-offs between modularity (isolation) versus performance overhead  
• Review these examples and the professor’s line‑of‑thinking as you prepare for the exam.

This list should help you focus on the concrete examples interleaved throughout the lecture that the professor signalled as likely exam topics. Make sure you can reconstruct the derivations and the design trade-offs on your own. Good luck studying!