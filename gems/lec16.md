### 1. Example: TA controls Canvas grade changes  
**Key Points**  
- Policy: Only TA should change grades  
- Attacks considered: bribing TA, physical access, breaking into Canvas server, breaking into TA or professor accounts  
- Security is a negative goal: proving the absence of unauthorized operations  
- Real-world implications of multiple attack vectors  

**Problem statement:**  
Your TA controls Canvas, which controls your grades. Policy states only the TA can change grades. What are the possible attacks to change grades if you want to cheat?  

**Solution:**  
- Bribing TA  
- Waiting for TA to leave their laptop, then changing grades  
- Breaking into Canvas servers  
- Hacking into TA's tech account  
- Breaking into professor's account  
The key lesson is that many attack possibilities exist; focusing only on one is insufficient. Security guarantees include detection by the professor noticing an attempt.  

_Summary: This example shows the complexity of defining policies and the range of attack vectors, emphasizing that security is about preventing all unauthorized operations, not just one scenario._

---

### 2. Example: Fairfax County superintendent password compromise  
**Key Points**  
- Policy flaw: teachers can add students to class and change password of any student in their class  
- Resulting failure: a 9-year-old student obtained access to the superintendent account  
- Illustrates how incorrect policies can lead to security breaches  

**Problem statement:**  
Fairfax County system policies:  
- Students can access their own files only  
- Superintendent can access all grades/files  
- Teachers can add new students to their class  
- Teachers can change passwords of any student in their class  
A 9-year-old student accessed the superintendent account. How?  

**Solution:**  
- The student added the superintendent as a student in a teacher's class  
- Changed the superintendent's password using teacher permissions  
- Logged in as superintendent  
This shows that the policy allowed teachers to effectively have unrestricted power when managing students, creating a fatal vulnerability.  

_Summary: Highlights importance of robust and well-thought-out policies. Even with mechanisms, bad policies can break security._

---

### 3. Example and Principle: Kerckhoffs’s Principle and Clipper Chip  
**Key Points:**  
- Kerckhoffs’s Principle: System is secure even if adversary knows everything except keys  
- Security cannot rely on secrecy of design ("security through obscurity")  
- Clipper Chip: example of secret government backdoor encryption that was broken when design got reverse-engineered  

**Problem statement:**  
Why is it dangerous to assume your system is secure because the design is secret? Example: Clipper Chip  

**Solution:**  
- The Clipper Chip was a government mandated encryption chip with a secret backdoor  
- A security researcher reverse-engineered and broke it, making the secret design insecure  
- Kerckhoffs’s Principle states system security must hold even if attacker knows the system  

_Summary: Fundamental design principle in security; always assume adversary knows system internals and design accordingly._

---

### 4. Example: Stuxnet and Threat Model Failures  
**Key Points:**  
- Stuxnet attacked air-gapped nuclear facility systems  
- Assumption that air-gapped systems could not be jumped was a flawed threat model  
- Real threat came from exploiting USB as an infection vector  

**Problem statement:**  
Stuxnet attacked Iranian nuclear centrifuges despite being air-gapped. How did that happen? What was wrong with the threat model?  

**Solution:**  
- Threat model assumed no network connection (air gap) means safety  
- Stuxnet used zero-day and USB to jump the air gap  
- Air gap assumption was invalid due to human and physical access vectors  

_Summary: Threat models must realistically capture attacker capabilities and environment to be effective._

---

### 5. Example: Buffer Overflow Vulnerability  
**Key Points:**  
- Vulnerability occurs when input length exceeds allocated buffer size  
- Stack memory can be overwritten, including return addresses  
- An attacker who controls the instruction pointer (IP) can execute arbitrary code  
- Illustrates memory safety and control flow hijacking  

**Problem statement:**  
Given code with a fixed-size buffer of size 10. If input length exceeds 10 (e.g., 100 bytes), what happens? What security risk arises?  

**Solution:**  
- Input overflows buffer, overwriting adjacent stack memory including return address  
- On function return, program jumps to attacker's chosen arbitrary address  
- Stack executable enables attacker to run shellcode  

_Summary: Classic example of how unchecked memory operations lead to critical security vulnerabilities; motivates use of memory-safe languages and protections._

---

### 6. Example: Password Storage and Hashing  
**Key Points:**  
- Naive storage of plaintext passwords is insecure  
- Hash passwords before storing, but simple hashing is vulnerable to rainbow table attacks  
- Use salted hashes (concatenate random nonce to password before hashing) to prevent precomputed attacks  
- Use slow hash functions to reduce brute force attacks  

**Problem statement:**  
How should a system store passwords securely to prevent password leaks being exploited? Explain the role of hashing and salting.  

**Solution:**  
- Hashing transforms arbitrary input to fixed-size output, irreversibly  
- Storing only hashes prevents getting plaintext from leaks  
- Rainbow tables allow attackers to precompute hashes for common passwords  
- Add a unique salt (random value) to each password before hashing, defeating precomputation  
- Slow hash functions (e.g., bcrypt, scrypt) further impede brute force  

_Summary: Standard approach to password security involves salted and slow hashes; understanding threat models is key to design._

---

### 7. Example: The C String Copy Vulnerability and Why Unsafe APIs Persist  
**Key Points:**  
- strcpy and similar functions lack bounds checking, leading to buffer overflows  
- Safer alternatives (e.g., strncpy) exist but legacy code uses unsafe APIs  
- The C language maintains unsafe APIs to preserve compatibility with legacy code  
- Languages like Rust attempt to avoid such unsafety  

**Problem statement:**  
Why does C still include unsafe string copy functions without bounds checking? What safer alternatives exist, and why aren't unsafe functions removed?  

**Solution:**  
- Backward compatibility is a major reason; removing APIs breaks legacy software  
- Safer bounded functions (strncpy) exist but are less widely used or have subtleties  
- Modern languages like Rust choose safety as a fundamental feature to avoid these errors  

_Summary: This reflects the tension between legacy system requirements and the pursuit of safer programming practices in security._

---

# Summary of Exam-Relevant Examples Found  
The lecture contains multiple concrete examples linked to fundamental security concepts, many of which the professor emphasized as possible exam material, including:  
- The Canvas grade manipulation attack (policy + multiple attack vectors)  
- The Fairfax County superintendent compromise (incorrect policies)  
- Kerckhoffs’s Principle illustrated by the Clipper Chip (security assumptions)  
- Stuxnet and threat model misassumptions (realistic adversary modeling)  
- Buffer overflow and memory safety (low-level vulnerability with exploitation details)  
- Secure password handling with hashing and salting (practical protection mechanisms)  
- Legacy unsafe C string functions and reasons for their existence (historical context in security)  

These examples highlight the professor’s approach: deriving security from foundational principles with real-world case studies and attack reasoning. They reflect the emphasis on understanding policies, mechanisms, threat models, and the failure cases leading to vulnerabilities, all critical for the exam.