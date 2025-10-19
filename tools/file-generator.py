# File 1: ASCII range 0-127 (including control characters 0-31)
ascii_range_with_controls = [
    "This is a test sentence using ASCII characters.",
    "Let's check how the program handles spaces and control characters.",
    "The quick brown fox jumps over the lazy dog.",
    "ASCII range includes control characters like newline (\\n) and tab (\\t).",
    "Control characters: " + chr(0) + " (NULL), " + chr(7) + " (Bell), " + chr(9) + " (Tab), " + chr(10) + " (Newline), " + chr(27) + " (ESC).",
    "\n",
    "\n",
    "\n",
    "\n",
    "\n",
    "Do we handle non-printable characters properly in the text files?",
    "" + chr(127) + " (DEL)",
    "\n",
    "\n",
    "\n",
    "\n",
    "The range 0-31 contains various control characters.",
    "End of the first file with ASCII control characters and regular text."
]

# File 2: Extended ASCII table (including control characters 0-31)
extended_ascii_with_controls = [
    "This is a test sentence with extended ASCII characters.",
    "Control characters like \\t (tab) and \\r (carriage return) can be included.",
    "Control characters: " + chr(0) + " (NULL), " + chr(7) + " (Bell), " + chr(9) + " (Tab), " + chr(10) + " (Newline), " + chr(27) + " (ESC).",
    "\n",
    "\n",
    "\n",
    "\n",
    "\n",
    "Extended ASCII includes characters for various languages and symbols.",
    "The quick brown fox jumps over the lazy dog with accents.",
    "Some extended characters are: " + chr(163) + " (Pound sign), " + chr(185) + " (Superscript one), " + chr(247) + "(Division sing).",
    "End of the second file with extended ASCII and control characters."
]

# Writing to File 1 (ASCII range 0-127 with control characters)
with open("sample-file-ascii.txt", "w") as f1:
    f1.write("\n".join(ascii_range_with_controls))

# Writing to File 2 (Extended ASCII table with control characters)
with open("sample-file-extended_ascii.txt", "w") as f2:
    f2.write("\n".join(extended_ascii_with_controls))
