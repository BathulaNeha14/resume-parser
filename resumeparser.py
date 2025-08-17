import re


class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_skill = False

class SkillTrie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, skill):
        node = self.root
        for word in skill.lower().split():
            node = node.children.setdefault(word, TrieNode())
        node.is_end_of_skill = True

    def search_skills(self, words):
        found_skills = set()
        n = len(words)
        for i in range(n):
            node = self.root
            current_skill = []
            for j in range(i, n):
                word = words[j]
                if word in node.children:
                    node = node.children[word]
                    current_skill.append(word)
                    if node.is_end_of_skill:
                        found_skills.add(' '.join(current_skill))
                else:
                    break
        return list(found_skills)


def extract_name(text):
    lines = text.strip().split('\n')
    return lines[0].strip() if lines else "Name not found"

def extract_email(text):
    return re.findall(r'\S+@\S+', text)

def extract_phone(text):
    return re.findall(r'\b\d{10}\b', text)

def tokenize(text):
    return re.findall(r'\b\w+\b', text.lower())


def calculate_match_percentage(extracted_skills, required_skills):
    matched = sum(1 for skill in extracted_skills if skill.lower() in map(str.lower, required_skills))
    return round((matched / len(required_skills)) * 100, 2) if required_skills else 0.0


def parse_resume(resume_text, required_skills):
    trie = SkillTrie()
    for skill in required_skills:
        trie.insert(skill)

    tokens = tokenize(resume_text)
    extracted_skills = trie.search_skills(tokens)
    match_percent = calculate_match_percentage(extracted_skills, required_skills)

    return {
        'Name': extract_name(resume_text),
        'Email': extract_email(resume_text),
        'Phone': extract_phone(resume_text),
        'Skills Found': extracted_skills,
        'Skill Match %': f"{match_percent}%"
    }


def input_resume():
    print("Paste the resume text below. End input with an empty line:")
    lines = []
    while True:
        try:
            line = input()
            if line == "":
                break
            lines.append(line)
        except EOFError:
            break
    return "\n".join(lines)

if __name__ == "__main__":
  
    required_skills = ['Python', 'Java', 'C++', 'SQL', 'Machine Learning', 'Data Structures']

    resume_text = input_resume()
    parsed_resume = parse_resume(resume_text, required_skills)

    for key, value in parsed_resume.items():
        print(f"{key}: {value}")
