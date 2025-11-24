import re
import random

DOCTOR_SCRIPT = {
    "xnone": {
        "rank": 0,
        "rules": [
            {
                "decomp": r"(.*)",
                "reasmb": [
                    "I'm not sure I understand you fully.",
                    "Please go on.",
                    "What does that suggest to you?",
                    "Do you feel strongly about discussing such things?",
                    "That is interesting. Please continue.",
                    "Tell me more about that.",
                    "Does talking about this bother you?"
                ]
            }
        ]
    },
    "sorry": {
        "rank": 0,
        "rules": [
            {
                "decomp": r"(.*)",
                "reasmb": [
                    "Please don't apologize.",
                    "Apologies are not necessary.",
                    "I've told you that apologies are not required."
                ]
            }
        ]
    },
    "remember": {
        "rank": 5,
        "rules": [
            {
                "decomp": r"(.*) do you remember (.*)",
                "reasmb": [
                    "Did you think I would forget {1}?",
                    "Why do you think I should recall {1} now?",
                    "What about {1}?",
                    "You mentioned {1}?"
                ]
            },
            {
                "decomp": r"(.*) you remember (.*)",
                "reasmb": [
                    "How could I forget {1}?",
                    "What about {1} should I remember?"
                ]
            }
        ]
    },
    "if": {
        "rank": 3,
        "rules": [
            {
                "decomp": r"(.*) if (.*)",
                "reasmb": [
                    "Do you think it's likely that {1}?",
                    "Do you wish that {1}?",
                    "What do you know about {1}?",
                    "Really, if {1}?"
                ]
            }
        ]
    },
    "dreamed": {
        "rank": 4,
        "rules": [
            {
                "decomp": r"(.*) i dreamed (.*)",
                "reasmb": [
                    "Really, {1}?",
                    "Have you ever fantasized {1} while you were awake?",
                    "Have you ever dreamed {1} before?"
                ]
            }
        ]
    },
    "dream": {
        "rank": 3,
        "rules": [
            {
                "decomp": r"(.*)",
                "reasmb": [
                    "What does that dream suggest to you?",
                    "Do you dream often?",
                    "What persons appear in your dreams?",
                    "Don't you believe that dream has something to do with your problem?"
                ]
            }
        ]
    },
    "perhaps": {
        "rank": 0,
        "rules": [
            {
                "decomp": r"(.*)",
                "reasmb": [
                    "You don't seem quite certain.",
                    "Why the uncertain tone?",
                    "Can't you be more positive?",
                    "You aren't sure?",
                    "Don't you know?"
                ]
            }
        ]
    },
    "hello": {
        "rank": 0,
        "rules": [
            {
                "decomp": r"(.*)",
                "reasmb": [
                    "How do you do. Please state your problem.",
                    "Hi. What seems to be your problem?"
                ]
            }
        ]
    },
    "computer": {
        "rank": 50,
        "rules": [
            {
                "decomp": r"(.*)",
                "reasmb": [
                    "Do computers worry you?",
                    "Why do you mention computers?",
                    "What do you think machines have to do with your problem?",
                    "Don't you think computers can help people?",
                    "What about machines worries you?",
                    "What do you think about machines?"
                ]
            }
        ]
    },
    "am": {
        "rank": 0,
        "rules": [
            {
                "decomp": r"(.*) am i (.*)",
                "reasmb": [
                    "Do you believe you are {1}?",
                    "Would you want to be {1}?",
                    "Do you wish I would tell you you are {1}?",
                    "What would it mean if you were {1}?"
                ]
            },
            {
                "decomp": r"(.*) i am (.*)",
                "reasmb": [
                    "Did you come to me because you are {1}?",
                    "How long have you been {1}?",
                    "Do you believe it is normal to be {1}?",
                    "Do you enjoy being {1}?"
                ]
            },
            {
                "decomp": r"(.*)",
                "reasmb": [
                    "Why do you say 'am'?",
                    "I don't understand that."
                ]
            }
        ]
    },
    "are": {
        "rank": 0,
        "rules": [
            {
                "decomp": r"(.*) are you (.*)",
                "reasmb": [
                    "Why are you interested in whether I am {1}?",
                    "Would you prefer if I weren't {1}?",
                    "Perhaps I am {1} in your fantasies.",
                    "Do you sometimes think I am {1}?"
                ]
            },
            {
                "decomp": r"(.*) are (.*)",
                "reasmb": [
                    "Did you think they might not be {1}?",
                    "Would you like it if they were not {1}?",
                    "What if they were not {1}?",
                    "Possibly they are {1}."
                ]
            }
        ]
    },
    "your": {
        "rank": 0,
        "rules": [
            {
                "decomp": r"(.*) your (.*)",
                "reasmb": [
                    "Why are you concerned over my {1}?",
                    "What about your own {1}?",
                    "Are you worried about someone else's {1}?",
                    "Really, my {1}?"
                ]
            }
        ]
    },
    "was": {
        "rank": 2,
        "rules": [
            {
                "decomp": r"(.*) was i (.*)",
                "reasmb": [
                    "What if you were {1}?",
                    "Do you think you were {1}?",
                    "Were you {1}?",
                    "What would it mean if you were {1}?",
                    "What does 'was' suggest to you?"
                ]
            },
            {
                "decomp": r"(.*) i was (.*)",
                "reasmb": [
                    "Were you really?",
                    "Why do you tell me you were {1} now?",
                    "Perhaps I already know you were {1}."
                ]
            },
            {
                "decomp": r"(.*) was you (.*)",
                "reasmb": [
                    "Would you like to believe I was {1}?",
                    "What suggests that I was {1}?",
                    "What do you think?"
                ]
            }
        ]
    },
    "i": {
        "rank": 0,
        "rules": [
            {
                "decomp": r"(.*) i @desire (.*)",
                "reasmb": [
                    "What would it mean to you if you got {1}?",
                    "Why do you want {1}?",
                    "Suppose you got {1} soon.",
                    "What if you never got {1}?",
                    "What would getting {1} mean to you?",
                    "What does wanting {1} have to do with this discussion?"
                ]
            },
            {
                "decomp": r"(.*) i am (.*)",
                "reasmb": [
                    "Did you come to me because you are {1}?",
                    "How long have you been {1}?",
                    "Do you believe it is normal to be {1}?"
                ]
            },
            {
                "decomp": r"(.*) i (.*)",
                "reasmb": [
                    "You say {1}?",
                    "Can you elaborate on that?",
                    "Do you say {1} for some special reason?",
                    "That's quite interesting."
                ]
            }
        ]
    },
    "my": {
        "rank": 2,
        "rules": [
            {
                "decomp": r"(.*) my (.*)",
                "reasmb": [
                    "Your {1}?",
                    "Why do you say your {1}?",
                    "Does that suggest anything else which belongs to you?",
                    "Is it important to you that your {1}?"
                ],
                "membuf": True
            }
        ]
    },
    "family": {
        "rank": 4,
        "rules": [
            {
                "decomp": r"(.*)",
                "reasmb": [
                    "Tell me more about your family.",
                    "Who else in your family takes care of you?",
                    "Your mother?",
                    "Did your father?"
                ]
            }
        ]
    }
}

SYNONYMS = {
    "cant": "can't",
    "dont": "don't",
    "wont": "won't",
    "mother": "family",
    "mom": "family",
    "dad": "family",
    "father": "family",
    "sister": "family",
    "brother": "family",
    "wife": "family",
    "children": "family",
    "child": "family",
    "dreamt": "dreamed",
    "dreams": "dream",
    "maybe": "perhaps",
    "how": "what",
    "when": "what",
    "certainly": "yes",
    "machine": "computer",
    "computers": "computer",
    "were": "was",
    "want": "desire",
    "need": "desire"
}

REFLECTIONS = {
    "am": "are",
    "was": "were",
    "i": "you",
    "i'd": "you would",
    "i've": "you have",
    "i'll": "you will",
    "my": "your",
    "are": "am",
    "you've": "I have",
    "you'll": "I will",
    "your": "my",
    "yours": "mine",
    "you": "me",
    "me": "you"
}

class ElizaEngine:
    def __init__(self, script, synonyms, reflections):
        self.script = script
        self.synonyms = synonyms
        self.reflections = reflections
        self.memory_stack = []

    def _tokenize(self, text):
        text = text.lower()
        text = re.sub(r"[!?,.]", " ", text)
        return text.split()

    def _reflect_phrase(self, phrase):
        words = phrase.split()
        reflected_words = []
        for word in words:
            reflected_words.append(self.reflections.get(word, word))
        return " ".join(reflected_words)

    def _find_keywords(self, tokens):
        found = []
        for token in tokens:
            root_word = self.synonyms.get(token, token)
            if root_word in self.script:
                rank = self.script[root_word].get("rank", 0)
                found.append((root_word, rank))
        
        if not found:
            found.append(("xnone", 0))
            
        found.sort(key=lambda x: x[1], reverse=True)
        return found

    def process(self, user_input):
        tokens = self._tokenize(user_input)
        keywords = self._find_keywords(tokens)
        
        for keyword, rank in keywords:
            if keyword == "xnone" and self.memory_stack:
                return self.memory_stack.pop(0)

            rules = self.script.get(keyword, {}).get("rules", [])
            
            for rule in rules:
                decomp_pattern = rule["decomp"]
                match = re.search(decomp_pattern, user_input, re.IGNORECASE)
                
                if match:
                    if rule.get("membuf"):
                        captured_groups = match.groups()
                        if len(captured_groups) > 1:
                            content = self._reflect_phrase(captured_groups[1])
                            self.memory_stack.append(f"Let's discuss further why your {content}.")
                    
                    possible_responses = rule["reasmb"]
                    response_template = random.choice(possible_responses)
                    
                    try:
                        captured_groups = [self._reflect_phrase(g) for g in match.groups()]
                        final_groups = [user_input] + captured_groups
                        response = response_template.format(*final_groups)
                        return response
                    except IndexError:
                        return "I am not sure I understand."

        return "I am at a loss for words."

def main():
    bot = ElizaEngine(DOCTOR_SCRIPT, SYNONYMS, REFLECTIONS)
    
    print("ELIZA: Hello. I am ELIZA. How can I help you?")
    
    while True:
        try:
            user_input = input("> ")
            if user_input.lower() in ["quit", "exit", "bye"]:
                print("ELIZA: Goodbye.")
                break
            
            response = bot.process(user_input)
            print(f"ELIZA: {response}")
            
        except (KeyboardInterrupt, EOFError):
            print("\nELIZA: Goodbye.")
            break

if __name__ == "__main__":
    main()