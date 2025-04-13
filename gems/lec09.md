Below is a detailed list of exam‐relevant examples and hints that the professor wove into this lecture. In many cases he “dropped” exam‐style questions (or phrasing such as “if I were to ask you…”) and emphasized particular examples or mechanisms that you should be able to reproduce on your own. Review these items carefully as you study:

──────────────────────────────
1. Fork Complexity with Full Copy Versus Lazy Copy
──────────────────────────────
• Example Statement in Lecture:
 – “If I were to ask you, basically, with vanilla XV6 with no modification whatsoever, what is the complexity of fork as a function of the number of physical frames?”
 – Immediately after, he states: “So the complexity of this is O(N).”
• Exam Hint:
 – You should be prepared to copy this question exactly, explain why a full copy (copying every physical frame) takes time proportional to the number of physical frames, and contrast it with the deduplication strategy (i.e. the lazy copy on write mechanism) that reduces the complexity to O(1) when no immediate copy is performed.
──────────────────────────────
2. Deduplication of Physical Frames on Fork
──────────────────────────────
• Example Statement in Lecture:
 – When discussing the alternative to copying all physical frames, the professor explains that the child process’s virtual frames are simply made to point to the same physical frames as the parent.
 – He then asks, “What is the complexity of that?” and answers “O(1).”
• Exam Hint:
 – You should be able to state and explain why deduping the physical frames (using a single update of pointers) is constant time and why that is “the best possible” compared to copying every frame.
──────────────────────────────
3. Triggering Copy on Write (CoW) When the Child Writes
──────────────────────────────
• Example Statement in Lecture:
 – The professor works through a scenario where after a fork the child attempts to write to its stack (pointed to by a red rectangle) even though by default the permission bits are set to “off” (to prevent writing on a shared frame).
 – He then explains: “Should we allow for this write to happen? … The answer is no, so we use copy on write.”
• Exam Hint:
 – Be ready to reproduce the reasoning: the child must have logical permission to write but not physical permission until a CoW is triggered. You should talk about how the trap occurs, a new physical frame (e.g., P1 prime) is allocated and the mapping updated, and then how permissions are reset so that the child can write.
──────────────────────────────
4. Updating Permission Bits in the CoW Process
──────────────────────────────
• Example Statement in Lecture:
 – The professor asks: “What should the page table entries look like for PT one prime? And what should PG two be?” 
 – He walks through that for the child’s mapping:
  ▪ The mapping for physical frame P3 (PG two) remains with the write bit turned off because it stays shared.
  ▪ The new copy P1 prime, which is unique to process two after the CoW, should have its write permission enabled.
• Exam Hint:
 – You should be able to write out the complete process. In an exam you may be given a diagram similar to that in the lecture and asked to mark the permission bits—zero (disabled) for shared frames and one (enabled) when the frame has been copied (and is uniquely referenced).
──────────────────────────────
5. Representing Memory Mapping as a Graph (Reference Counting)
──────────────────────────────
• Example Statement in Lecture:
 – The professor introduces a conceptual “directed graph” where each vertex is a page or page table entry, and the edges capture sharing.
 – He even mentions an “adjacency matrix” mental model and asks you to think about finding the number of unique paths (reference count) pointing to a physical frame.
• Exam Hint:
 – Be ready to explain how the operating system determines if a physical frame is shared (accessible from more than one process) using a reference count or graph traversal idea. Remember the key point: if more than one process (or page table) points to the frame, then a CoW copy is required.
──────────────────────────────
6. TLB Invalidation Question Related to a CoW Update
──────────────────────────────
• Example Statement in Lecture:
 – At one point the professor poses a “trick question”: “How many TLB (Translation Lookaside Buffer) invalidates do we need to make on a write to P1?” He offers multiple possibilities (0, 42, etc.) and explains the detailed reasoning.
 – The answer he arrives at is “one.” He explains that only one invalidate is needed on the process’s context currently in the kernel.
• Exam Hint:
 – You should be prepared to write out the reasoning process: when a page mapping changes (the VFN to PFN mapping, along with updated protection flags), only the affected entry in the TLB of the running process needs to be flushed (or replaced), because the update is local to that process’s context.
──────────────────────────────
7. Handling Break and Lazy Allocation (Zero-Filled Pages)
──────────────────────────────
• Example Statement in Lecture:
 – Later in the lecture, when discussing lazy allocation, the professor walks through an example where a process’s break call allocates two new virtual pages.
 – Instead of mapping two separate physical pages, the system can map both VfNs to the one shared (zero‐filled) physical frame and later trigger CoW when a write occurs.
• Exam Hint:
 – You should be ready to explain the savings in physical memory from this strategy, how read-only mapping works until modification is needed, and the role of the “copy on write” mechanism in reassigning a unique physical frame.
──────────────────────────────
8. Mapping a Shared Library Code Segment (libc) Example
──────────────────────────────
• Example Statement in Lecture:
 – The professor examines the memory map of processes (using /proc/PID/maps) and discusses a shared mapping of the libc shared object. He points out that the mapping is page-aligned (all addresses’ three least significant hexadecimal digits are zero).
 – He computes the size of the mapping by subtracting the start (e.g., c00 hex) from the end (e.g., D8A hex) to obtain a size (18A hex) and then asks: “How many page table pages do we need to maintain this mapping?” The answer is “just one” because one page table page can cover the range.
• Exam Hint:
 – You might be asked to perform similar calculations. Be prepared to:
  ▪ Convert hexadecimal address ranges,
  ▪ Remember that page size is 2^12 (or 0x1000) bytes and that addresses are page aligned,
  ▪ And determine how many entries (or page table pages) are needed given typical limits (e.g., 1024 entries in a 32‑bit page table or 512 in a 64‑bit system).
──────────────────────────────
9. Estimating the Number of Page Table Pages for a Large Memory Region
──────────────────────────────
• Example Statement in Lecture:
 – Near the end, the professor introduces a thought exercise: “If you’re mapping 1 gigabyte of memory, how many page table pages (PTPs) do we need?” He leaves it as a thought exercise but makes clear that the answer involves calculating the number of pages (2^30 / page size) and then comparing it to the capacity of one page table page.
• Exam Hint:
 – You should know how to calculate the number of pages in a given memory region and understand the relationship between virtual addresses, page sizes, and the structure of page tables.
──────────────────────────────
10. Overall Concept: Propagation of Mapping Changes Through the Hierarchy
──────────────────────────────
• Example Statement in Lecture:
 – Throughout the lecture, particularly when talking about the cascade of changes required during a CoW event (copying the physical frame, then the last-level page table page, and finally updating the page directory entry), the professor repeatedly emphasizes that “everything can be derived from first principles.”
 – He stresses that even if you have a multi-level structure (parent, child, grandchild processes) you should conceptualize updates as changes in a “graph” of mappings.
• Exam Hint:
 – Be ready to describe (and possibly draw) the complete process of a CoW 'write' event starting from the trap, copying the physical memory, updating page table entries and directory entries, and then propagating the change (and performing TLB invalidates) accordingly.
──────────────────────────────
General Advice:
• Many of these items are not isolated trivia but part of a deeper conceptual framework. The professor urged that you follow his “first principles” approach—explain everything from the basic definitions of virtual memory mappings, permission bits (logical vs. physical), and the flow of a fork (and subsequent writes).
• When studying, try to solve for yourself every “if I were to ask you…” example that was mentioned.
• For each example (especially the ones above), make sure you can reproduce the problem statement and the complete chain of reasoning (as given by the professor).

Use this list as a guide while reviewing the lecture recordings and your notes to ensure you’re covering all exam-relevant details.