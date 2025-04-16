### 1. Setup of entry PGDR and Memory Aliasing at Boot Time  
**Key Points**  
- At the end of bootstrapping, two virtual pages (virtual frame numbers) are mapped to the same physical frame (memory aliasing).  
- One virtual page at the very bottom of virtual memory and another starting at current base map to the same 4MB physical frame.  
- After kernel boot, the low address entry is deleted and replaced with per-process user-space mappings.  

_No explicit exam problem here, but fundamental understanding of page directory setup and memory aliasing after boot is emphasized._

---

### 2. Meaning and Effects of Bits in Page Directory Entry (PDE) and Page Table Entry (PTE)  
**Key Points**  
- Most significant 20 bits store physical page number (PFN) pointing to next level page table (in PDE) or physical frame (in PTE).  
- Least significant 12 bits store flags: present, writable, user/supervisor, disable cache, accessed, dirty, page size (4KB or 4MB page).  
- Present bit is ultra important (lab two).  
- Page size bit indicates whether entry points to 4KB page (PS=0) or 4MB page (PS=1).  

_Important fundamental knowledge for exam: knowing bits’ meanings and their role in paging, especially the present bit and page size bit._

---

### 3. Example: Comparing Single-Level and Two-Level Paging Structures  
**Problem statement:**  
What if we combine the 10 + 10 most significant bits into a single level page table index? What are the implications for page directory size and memory overhead?

**Solution:**  
- Single-level indexing with 20 bits means page directory has 2^20 entries.  
- Each entry is 4 bytes (32-bit system). Size = 2^20 * 4 bytes = 4 MB just for one page directory.  
- With many processes, this overhead multiplies (e.g., 1024 processes × 4 MB = 4 GB overhead).  
- Two-level paging splits indexing (10 & 10 bits) to reduce size of the page directory but involves more memory references.  
- Large pages (4MB) reduce overhead but waste memory if process uses little memory; small pages (4KB) are efficient for small processes but increase size of page directory.  
- Tradeoff: optimizing either memory overhead or latency overhead rarely both simultaneously.  

_If I were to ask you this on the exam: describe memory overhead tradeoffs in single-level versus two-level paging._

---

### 4. How Many Memory Accesses to Translate VA to PA in Two-level Paging?  
**Problem statement:**  
How many memory operations does a two-level page table walk take for virtual-to-physical address translation?

**Solution:**  
- Perform one memory read for page directory to get page table pointer.  
- Perform second memory read for page table to get physical frame number.  
- Total two memory reads (plus actual memory access after translation).  

_Emphasized answer for the exam: answer is 2 memory reads for the page table walk in two-level paging._

---

### 5. Three Paging Design Choices: Splitting Linear Address and Their Tradeoffs  
**Key Points:**  
- Canonical 2-level paging: split 10 bits / 10 bits / 12 bits.  
- Single-level with large pages: small page directory (1024 entries = 4KB), frames are 4MB pages.  
- Single-level with large page directory: page directory has 1 million entries (4 MB), frames are 4KB pages.  
- Small processes: cost in frames allocation differs; large pages wastes memory, large page directories waste memory on directory metadata for many processes.  
- Tradeoff between latency (walk steps) and memory overhead.  

_Principle for exam: understand design tradeoffs and how bit splits affect sizes of page tables and physical frames._  

---

### 6. Example: Number of Page Table Entries in 64-bit System and Four-Level Paging  
**Problem statement:**  
Given a 64-bit system using 48 bits of virtual address and 4KB page tables, how is the linear address split, and how many entries fit in a page directory or page table?

**Solution:**  
- Page size 4 KB = 2^12 bytes offset.  
- 48 bits used for VA minus 12 bits offset leaves 36 bits.  
- Page table entries are 64 bits = 8 bytes each.  
- Number of entries per page (4KB/8B) = 512 entries = 2^9 entries per table.  
- So 36 bits split into four chunks of 9 bits each for indexing four levels of page tables.  
- Hence, the X86-64 system uses 4-level paging with indices of 9 bits each in PML4, PDPT, PD, PT.  
- Each lookup reads one level, so total 5 memory operations (4 lookups + 1 actual data memory operation).  

_If I were to ask this on the exam: explain address splitting in X86-64 paging and size of page tables._

---

### 7. Example: WalkPGDIR Code Walkthrough for VA to PA Translation in XV6  
**Problem statement:**  
Describe the steps of xv6 function `walkpgdir` which takes a virtual address (VA), page directory (PGDR), and a flag to allocate a page table if missing, and returns a pointer to the page table entry.

**Solution:**  
- Extract top 10 bits (PGX) from VA to index into page directory.  
- Get PDE pointer `pde = &pgdir[PGX(VA)]`.  
- Check present bit in PDE. If not present and allocation flag is set:  
  - Allocate new page for page table.  
  - Zero out page table (clear flags including present bit).  
  - Update PDE with physical address of new page table with present, writable, user bits set.  
- If present bit is set:  
  - Extract physical address of page table from PDE.  
  - Convert physical address to virtual address with p2v (physical to virtual).  
  - Cast to page table pointer.  
- Extract next 10 bits (PTX) from VA to index into page table.  
- Return pointer to PTE: `&(pagetable[PTX(VA)])`.  

_If I were to ask you this on the exam: explain or write code for two-level page walk given a VA and page directory._

---

### 8. Important Exam Hints Related to Present Bit and Allocation in walkpgdir  
**Key Points:**  
- Present bit in PDE crucial for deciding if page table needs to be allocated.  
- Allocation zeroes out page table page to clear flags including present bit.  
- Present and writable and user bits set explicitly on PDE after allocation.  
- Extracting PGX and PTX bits uses right shifting and masking (`>>` and `& 0x3FF`).  
- Indexing into page directory/table as arrays with these indices.  

_This is emphasized as ultra important for lab two and for exam: understanding page walk implementation and role of present bits._

---

### 9. Entry Point Boot Allocation and Loading Entry PGDR  
**Key Points:**  
- At boot, kernel sets CR4 flags to enable 4MB pages.  
- Loads physical address of entry PGDR into CR3 (page directory base register).  
- CR3 requires physical address, not virtual.  
- Entry PGDR sets up aliasing: virtual frame numbers 0 and 512 point to same physical 4MB frame.  

_If I were to ask you this on the exam: describe how CR3 is loaded and what is the significance of entry PGDR and its mapping._

---

### 10. Why XV6 Cannot Support Copy-on-Write or Shared Memory as Is  
**Key Points:**  
- XV6 currently maps physical pages one-to-one to virtual pages (no multiple virtual pages to the same physical frame).  
- This precludes copy-on-write and shared memory implementation in current XV6.  
- UNIX systems support many-to-one mapping allowing copy-on-write and shared libraries.  
- Copy-on-write requires tracking multiple VFNs mapping to same physical frame, needing reference count metadata.  

_Exam-relevant concept: limitations of XV6 memory system compared to more advanced OSs, especially regarding shared memory and copy-on-write support._

---

### 11. TLB and Its Interaction with Page Table Design Choices  
**Key Points:**  
- TLB caches VA to PTE mappings to speed up virtual-to-physical translation.  
- TLB entries map virtual frame numbers to page table entries (which hold physical frame number and flags).  
- Given fixed TLB size (e.g., 128 entries), larger page sizes (e.g., 4MB pages) increase amount of memory each TLB entry covers, improving hit ratio.  
- Choosing between large page directory with small frames or small page directory with large frames affects TLB performance drastically.  
- Attendees’ discussion: splitting TLB into ITLB (instruction) and DTLB (data) improves locality and reduces flushes.  

_If I were to ask: explain the impact of page size on TLB hit rate and why TLB may be split into instruction and data caches._

---

This thorough review extracts all key conceptual examples and exam hint moments the professor emphasized, including code walkthroughs, design tradeoffs, bit-level details, and interactions among paging, TLB, and memory overhead.