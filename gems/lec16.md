Below is a list of the examples from the lecture that the professor emphasized (or “dropped hints” about) as potential exam–style problems. In each case I’ve (1) “copied” the problem scenario (or question) as stated by the professor and (2) summarized his solution or line‐of–reasoning. (Note that the professor sometimes “rhetorically” posed the challenge in class; the versions below are my extracted “exam candidates” based on his hints. You should be sure you can work through each one from first principles!) 

──────────────────────────────
1. TA/Canvas Grade Attack Scenario

• Problem statement (as given in lecture):  
  “Your TA controls Canvas, which ultimately controls your grade. The policy is that only the TA should be able to change grades in Canvas. Now imagine that you’re unhappy with a grade. What might you do? In other words, what are the potential attack vectors or ways to ‘cheat’ this system?” 

• Professor’s solution/line of reasoning:  
  He mentioned that a student could try several routes—for example, bribing the TA, waiting for the TA to leave their laptop unattended and then logging in (or even physically accessing the TA’s machine), or even attacking the Canvas servers (or compromising a TA’s tech account). He emphasized that there is a “ton of attacks” available and that thinking through each shows the many ways that policy can fail.  
  Remember: This example shows that security is “a negative goal” (i.e. it’s about proving the absence of failures) and that even one successful breach (even by bribing or stealing credentials) is enough to break the guarantee.

──────────────────────────────
2. Fairfax County Policy Failure Example (“Superintendent Access”)

• Problem statement:  
  “In a real case from Fairfax County, Virginia, a 9‐year‐old boy was caught accessing a gray–management account owned by the superintendent. The system policies were:  
   – A student can access only their own files.  
   – The superintendent can access everyone’s files (grades, etc.).  
   – Teachers can add new students to their class.  
   – Teachers can change the password of any student in their class.  
  Yet somehow, the student got access to everything—as if they were the superintendent. How did this happen?”

• Professor’s solution/line of reasoning:  
  He explained that the bug was in the policy management: a teacher (or someone in that chain) could both add the superintendent as a student in a teacher’s class and then change the password for that “student.” In effect, by misusing the privilege normally reserved for teachers, the student ended up gaining the same access as the superintendent.  
  Note: This example illustrates how bad policy design (or mismanagement of policy administration) can lead to catastrophic privilege escalation.

──────────────────────────────
3. Buffer Overflow Vulnerability in C Code

• Problem statement (as “posed” in lecture):  
  The professor showed a short function (named for example “Quit”) that copies input into a fixed–size buffer without checking whether the input exceeds the buffer length. He then asked, “Can someone tell me what’s wrong with this function?”

• Professor’s solution/line of reasoning:  
  The answer: if the input size is greater than the allocated size (e.g. a buffer defined to hold 10 characters), copying a longer input causes a buffer overflow. This can overwrite important data on the stack, such as the base pointer or the return address (IP). If the return address is overwritten with a malicious value, an attacker can gain control of the program and execute arbitrary code (for example by “jumping into” the injected code on the stack).  
  Key point: Always check that the amount of data written to a buffer does not exceed the buffer’s size.

──────────────────────────────
4. Password Storage, Hashes, and Rainbow Tables

• Problem statement:  
  “Consider the common scenario for storing user passwords. One simple (but naive) solution is to store the plain–text password. A better approach is to store a hash of the password. But if you compute H(password) and store it, an attacker who gets the hash might simply try common passwords until one produces the same hash. How does adding a random value (‘salt’) help, and what are the remaining vulnerabilities if the salt (R) is stored in the clear?”

• Professor’s solution/line of reasoning:  
  He explained that by concatenating a password with a random salt R (i.e. storing H(password || R)), you “force” an attacker to recompute the hash for each guess because pre–computed tables (rainbow tables) are no longer effective. Even though R is stored on disk and known to attackers, its purpose is to slow down dictionary and brute–force attacks. However, if the password itself is weak or very common, an attacker may still eventually try enough guesses (even with the salt) to compromise weak passwords.  
  This example emphasizes the importance of using proper salting and slow hash functions to defend against pre–computed dictionary attacks.

──────────────────────────────
5. “Kerckhoffs’s Principle” (Referred to as “Karkovs Principle”)

• Problem statement:  
  “Explain the principle that states ‘the system must be secure even if the adversary knows everything about it’ (i.e. Kerckhoffs’s Principle). What does this imply about relying on ‘security through obscurity’?”

• Professor’s solution/line of reasoning:  
  He underscored that one of the cornerstones of good security design is that an adversary knowing the inner workings of the system should still not be able to break it. In other words, hiding the design (obscurity) is not a substitute for solid security mechanisms.  
  This principle is its own exam candidate because it underpins many of the design decisions in security engineering.

──────────────────────────────
6. The Clipper Chip Example

• Problem statement:  
  “The Clipper Chip was a government–mandated encryption chip with a built–in backdoor, designed so that only law enforcement (or US persons) could later break the encryption. Explain the fundamental design flaw demonstrated by the Clipper Chip.”

• Professor’s solution/line of reasoning:  
  He explained that although the Clipper Chip was intended to provide secure cryptography with a controlled backdoor, in practice the chip’s design was kept secret. A former research scientist eventually reverse–engineered it and showed that once the secret design was exposed, the backdoor could be exploited by adversaries. This example illustrates that relying on secrecy of design (or “security by obscurity”) is a flawed approach.  
  It also demonstrates that a flexible adversary will eventually uncover hidden design details if they can get hands on the device.

──────────────────────────────
7. Supply Chain/Third–Party Attacks: Xcode Host and Left–Pad

• Problem statement:  
  “Discuss two examples of supply–chain attacks presented in lecture: one involving the Xcode host (where malicious code was injected into compiled apps) and one involving the left–pad incident in the NPM ecosystem. What went wrong in each case?”

• Professor’s solution/line of reasoning:  
  For Xcode host, the professor recounted that compromised third–party servers (originally set up to host Xcode updates) ended up injecting malware into a huge number of apps, exposing an entire ecosystem of software to attack. For left–pad, someone gained control of the namespace in the central code–repository (NPM) and replaced a critical small library (used to “left pad” strings) with malicious code, which then broke hundreds or thousands of applications.  
  These examples show how weaknesses in the ecosystem (or management of third–party dependencies) can lead to vulnerabilities far beyond the immediate codebase.

──────────────────────────────
8. Memory Safety and the Need for Safe Languages

• Problem statement:  
  “Memory–safety vulnerabilities (like buffer overflows, use–after–free, and timing attacks) have been a persistent problem in systems written in C. Describe a common code–based example (such as the buffer overflow in the ‘Quit’ function) and explain why a memory–safe language (e.g. Rust) is a promising solution.”

• Professor’s solution/line of reasoning:  
  Using his example of a function that copies more characters into a fixed–sized buffer than it can hold, he detailed how such an overflow can override the stack’s return address (among other critical data) and allow an attacker to execute arbitrary code. He then pointed out that modern efforts (for instance, in the Linux community) are moving toward memory–safe languages (like Rust) to avoid these pitfalls.  
  The core idea is that by having language–level safety checks, many such vulnerabilities can be prevented at compile time or runtime rather than after deployment.

──────────────────────────────
9. Air–Gap Assumptions and USB/Zero–Day Exploits (e.g. Stuxnet)

• Problem statement:  
  “Air–gap systems are assumed to be safe simply because they are not connected to the network. Yet examples like Stuxnet have shown that even air–gapped systems can be compromised. How can an attacker breach an air–gap system?”

• Professor’s solution/line of reasoning:  
  He explained that attackers have used zero–day vulnerabilities in processing of USB media to “jump” the gap. The assumption that the air–gap makes the system inaccessible is undermined if the attacker can supply malicious code through removable media. This example emphasizes that even seemingly isolated systems cannot be assumed secure.

──────────────────────────────
10. Timing Attacks and Side Channels

• Problem statement:  
  “Describe how a timing attack can leak information about secret values (such as password comparisons) and explain why such side–channel attacks represent a serious risk.”

• Professor’s solution/line of reasoning:  
  He noted that if the time taken to perform an operation (such as a string or memory comparison) varies with the input, an attacker can use carefully measured differences in processing time to deduce information about correct values. For example, if a function returns faster when the first character does not match, that information itself is a leak that an attacker can exploit.  
  This demonstrates that even low–level implementation choices have significant security implications.

──────────────────────────────
11. Trusting Hardware (Farewell Dossier Case)

• Problem statement:  
  “Using the example of the Farewell Dossier mentioned in class, explain why relying solely on the provenance and trustworthiness of hardware can be dangerous.”

• Professor’s solution/line of reasoning:  
  He described how even trusted hardware components (such as those embedded in critical infrastructure) can be subverted. In the Farewell Dossier case, supposedly “trusted” US–provided hardware was later found to be deliberately flawed (causing defective turbines, misleading information, etc.) and ended up sabotaging Soviet systems.  
  The key takeaway is that blind trust in the supply chain—even at the hardware level—can lead to catastrophic vulnerabilities.

──────────────────────────────

These examples, with their corresponding “problems” and solutions outlined by the professor, are all candidates for exam questions. Be sure to not only recall these scenarios but also work through the reasoning behind each example from first principles. If the professor ever phrases “if I were to ask you this on the exam…” in future lectures, you now know to pay extra attention to details in these cases.

Make sure you fully understand each example such that you can solve similar ones on your own. Happy studying!