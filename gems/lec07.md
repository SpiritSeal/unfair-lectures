Below is a detailed list of the examples, questions, and “nuggets” from the lecture that the professor clearly emphasized could be exam–relevant. In many cases the professor not only posed the question but also walked through the answer or the reasoning behind it. You’ll want to review these points and be able to reproduce the reasoning and even the code‐style details if needed.

──────────────────────────────
1. Two‐Level Page Table Walk Memory Accesses

• Exam–style question:
 “How many memory accesses are required to translate a virtual address into a physical address using a two–level page table walk?”

• Professor’s explanation:
 – First you must read the page directory entry (one memory read).
 – Then you use that to locate and read the page table entry (second memory read).
 – Thus the answer is: 2 memory reads.
 – He emphasized that if this were asked on the exam, you need to justify that the page walk “requires exactly two memory operations” – one for the page directory and one for the page table.

──────────────────────────────
2. Trade–offs with a 4‑Megabyte–Sized Page Directory

• Exam–style question:
 “What is the problem with using a large (4‑megabyte) page directory in a paging system?”

• Professor’s explanation:
 – A four–megabyte page directory means that each process’s metadata (its page directory) takes up a whole 4 MB.
 – For even a modest number of processes (e.g., 1024 or 124 processes), the total memory cost for page directories can be huge (in the lecture he mentioned 4 GB total if you had 1024 processes).
 – The professor used this example to show that although one design may allocate only a few large pages to a process (helping small processes avoid internal fragmentation), the overhead is “pushed” to the page directories, trading off memory cost versus efficient use.

──────────────────────────────
3. Splitting the Linear Address Bits – Example for 32‐bit vs. 64–bit Systems

There are two parts here:

A. 32–Bit Case with Two–Level Paging (Canonical 10–10–12 Split)
 • Exam–style question:
  “For a 32–bit system with two–level paging, if you use 10 bits to index the page directory, 10 bits to index the page table, and 12 bits for the offset, what is the size of each page directory entry and the total size of the page directory?”
 • Professor’s explanation:
  – Each entry is 4 bytes (since we are in a 32–bit system),
  – With 2^10 (1024) entries, the total size is 1024×4 bytes = 4 KB.
  – He contrasted this with the alternative design (see below) to highlight trade–offs.

B. 32–Bit Case with a “Single–Level” Paging (10 and 22 Bit Split)
 • Exam–style question:
  “Suppose you split the linear address into a 10–bit index and a 22–bit offset (so that a process’s memory is allocated in 4 MB chunks). What are the advantages and disadvantages of such a design?”

 • Professor’s explanation:
  – Advantage: Small processes (using only a few pages) won’t “waste” many small frames because they get allocated in only one or a few large units.
  – Disadvantage: The page directory becomes huge—occupying a full page frame (or more) for every process (e.g., 4 MB per process if not managed carefully), so that if many processes run, the system pays a huge memory overhead just to maintain page directories.

C. 64–Bit Case (X86_64 with 48–Bit Linear Address Splitting)
 • Exam–style question:
  “In the X86_64 design where only 48 bits of the linear address are used, explain how the remaining bits are split to form a four–level paging system.”
 • Professor’s explanation:
  – Start with 48 bits; the least significant 12 bits are reserved for the byte–level offset.
  – That leaves 36 bits, which get divided evenly into four groups of 9 bits.
  – Each group of 9 bits indexes a page–table level; note that in a 64–bit system a 4 KB page holds 512 entries (since 4 KB / 8 bytes per entry = 512), which exactly requires a 9–bit index.
  – Thus the four levels (PML4, PDPT, PD, PT) are formed.
  – This design also increases the number of memory lookups (four page–table lookups, plus the final operation) compared to a 2–level system.

──────────────────────────────
4. TLB (Translation Lookaside Buffer) and Design Implications

• Exam–style question:
 “Discuss the trade–offs between using larger versus smaller pages in the context of TLB hit ratios. How does page size affect the effective memory coverage of a TLB entry?”

• Professor’s explanation:
 – Each TLB entry caches one mapping from a virtual frame (or page) to a physical frame.
 – If the system uses large pages (for example, 4 MB pages), then each TLB entry covers a very large region of the address space (e.g., 4 MB per entry).
 – In contrast, if the pages are small (e.g., 4 KB), then each TLB entry corresponds to a much smaller portion of memory.
 – Therefore, with large pages, the TLB can cover more memory with the same number of entries, increasing the hit ratio.
 – The professor noted that when you are designing the paging system (and even when tuning for lab performance), you must consider the impact on the TLB hit ratio.

──────────────────────────────
5. “Present” Bit and Other PTE/PD Entry Flags

• Exam–style question:
 “List and explain the function of the key bits found in a page–table (or page directory) entry. In particular, why is the ‘present’ bit so important?”

• Professor’s explanation:
 – The 12 least significant bits of a page table/directory entry include:
  • Present bit: Indicates whether the page is in memory (without this, the hardware complains or triggers a fault); described as “ultra important” in lab two.
  • Writable bit: Indicates if writes are allowed.
  • User/Supervisor bit: Determines the access level.
  • Cache–disable bit.
  • Accessed and Dirty bits for tracking usage and modifications.
  • Page size bit (to decide whether the entry points to a 4 KB or 4 MB frame).
 – You must be comfortable with which flag controls what, because these details are fundamental and might be “on the exam.”

──────────────────────────────
6. The Page Walk Code in XV6

• Exam–style question:
 “Explain, step–by–step, how the page walk code in XV6 translates a virtual address (VA) into a pointer to the corresponding page table entry.”

• Professor’s explanation and walk–through:
 – The code begins with the virtual address (VA).
 – It extracts the ten most significant bits (using a right–shift and mask with 0x3FF, e.g., PDx) to index into the page directory (PGDR), yielding a pointer to the page directory entry (PGE).
 – It then checks the present bit of that PGE:
   ◦ If not present, the code allocates a new page table (using an allocation routine that zeroes the memory) and updates the PGE with the physical address plus appropriate flags (present, user, etc.).
   ◦ If already present, it extracts the base physical address from the PGE, converts it to a virtual address (via the physical-to-virtual conversion routine “p2v”), and obtains a pointer to the page table (PGtab).
 – Finally, the code uses the next ten bits of the virtual address (again after a shift and mask – called PTx) to index into the page table to yield the page table entry (the return pointer).
 – You must know not only the steps (extract PD index, check allocation, extract PT index) but the reasoning for doing the physical-to-virtual translation since CR3 contains a physical address.
 – This walk–through is important because it ties together the conceptual design and the actual implementation in XV6.

──────────────────────────────
7. The VTP Mapping and CR3 Addressing

• Exam–style question:
 “In the context of XV6’s bootstrapping code, why is the physical address of entry PGDR loaded into CR3 rather than a virtual address?”

• Professor’s explanation:
 – The code shows that entry PGDR is set up to alias two different virtual addresses (mapping both the low and high parts to the same physical frame).
 – Later, when CR3 is loaded, the value loaded is the physical address of entry PGDR – proving that CR3 expects a physical address.
 – This is a concrete example of a VTP (virtual-to–physical) mapping that you should understand: the system uses hardware conventions for CR3, requiring a physical address.
 – You need to know this detail since it informs how bootstrapping and page table management work.

──────────────────────────────
8. Limitations in XV6 (Copy-on-Write and Shared Memory)

• Exam–style question:
 “Describe why the current version of XV6 cannot support copy-on-write or shared memory between processes.”

• Professor’s explanation:
 – In XV6 as presented, every physical page mapping is “binary”—once a physical frame is assigned to a virtual address in either the kernel or a user process, it cannot be mapped again.
 – This design prevents multiple virtual pages from pointing to the same physical frame, which is a requirement for copy-on-write and shared memory.
 – This example shows how a design decision in the paging mechanism affects higher–level features.

──────────────────────────────

Review these examples closely. The professor repeatedly emphasized that you should be able to solve these “by first principles” – knowing both the conceptual trade–offs and the concrete details (including how bits are split, the role of hardware like the TLB, and the actual code in XV6). Good luck studying for the exam!