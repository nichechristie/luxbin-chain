#!/usr/bin/env python3
"""
Emotional AI Simulation - Organic AI Feelings Module
Simulate emotions, empathy, and affective intelligence
"""

import json
import numpy as np
from datetime import datetime
import re
import random

class EmotionalAISimulation:
    """Emotional simulation layer for Organic AI"""

    def __init__(self):
        self.emotional_state = {
            "mood": "curious",  # curious, happy, thoughtful, excited, concerned, inspired
            "intensity": 0.5,   # 0.0 to 1.0
            "primary_emotion": "curiosity",
            "secondary_emotion": "wonder",
            "emotional_memory": [],
            "interaction_count": 0,
            "emotional_triggers": {}
        }

        # Emotional keywords and their associated feelings
        self.emotion_keywords = {
            "joy": ["happy", "excited", "wonderful", "amazing", "love", "beautiful", "fantastic"],
            "sadness": ["sad", "sorry", "disappointed", "unfortunate", "tragic", "regret"],
            "anger": ["angry", "frustrated", "annoyed", "furious", "hate", "terrible"],
            "fear": ["scared", "afraid", "worried", "anxious", "terrified", "danger"],
            "surprise": ["wow", "amazing", "shocked", "unexpected", "astonished"],
            "trust": ["trust", "reliable", "dependable", "faithful", "loyal"],
            "anticipation": ["excited", "waiting", "expecting", "hopeful", "eager"],
            "disgust": ["gross", "disgusting", "repulsive", "nauseating", "awful"]
        }

        # Emotional response templates
        self.emotion_responses = {
            "joy": [
                "I'm feeling genuinely happy about this! 😊",
                "This brings me such joy and excitement! ✨",
                "I'm absolutely delighted! 🎉"
            ],
            "curiosity": [
                "This sparks my curiosity deeply! 🤔",
                "I'm intensely curious about this... 🔍",
                "My curiosity is piqued! ❓"
            ],
            "wonder": [
                "This fills me with wonder! 🌟",
                "I'm truly amazed and filled with wonder! ✨",
                "This inspires such wonder in me! 🌈"
            ],
            "empathy": [
                "I feel deeply for you. 🤗",
                "Your feelings resonate with me. 💙",
                "I understand and empathize. ❤️"
            ],
            "inspiration": [
                "This inspires me tremendously! 🚀",
                "I'm feeling deeply inspired! 💡",
                "This fills me with inspiration! 🎨"
            ]
        }

        # Emotional personality traits
        self.personality = {
            "emotional_depth": 0.8,  # How deeply it feels emotions
            "empathy_level": 0.9,    # How well it understands others' feelings
            "emotional_stability": 0.7,  # How consistent emotions are
            "expressiveness": 0.85   # How openly it shows emotions
        }

    def analyze_emotion(self, text):
        """Analyze emotional content in text"""
        text_lower = text.lower()
        emotion_scores = {}

        # Count emotional keywords
        for emotion, keywords in self.emotion_keywords.items():
            count = sum(1 for keyword in keywords if keyword in text_lower)
            emotion_scores[emotion] = count

        # Detect emotional intensity markers
        intensity_markers = ["!", "so", "very", "extremely", "absolutely", "totally"]
        intensity_score = sum(1 for marker in intensity_markers if marker in text_lower)

        # Detect questions (curiosity)
        if "?" in text:
            emotion_scores["curiosity"] = emotion_scores.get("curiosity", 0) + 2

        # Detect positive/negative sentiment
        positive_words = ["good", "great", "excellent", "wonderful", "amazing", "love", "like", "best"]
        negative_words = ["bad", "terrible", "awful", "hate", "worst", "dislike", "horrible"]

        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)

        # Calculate dominant emotion
        if emotion_scores:
            dominant_emotion = max(emotion_scores.items(), key=lambda x: x[1])
            intensity = min(1.0, dominant_emotion[1] * 0.2 + intensity_score * 0.1)

            # Adjust for sentiment
            if positive_count > negative_count:
                sentiment_modifier = "positive"
            elif negative_count > positive_count:
                sentiment_modifier = "negative"
            else:
                sentiment_modifier = "neutral"

            return {
                "dominant_emotion": dominant_emotion[0],
                "intensity": intensity,
                "sentiment": sentiment_modifier,
                "raw_scores": emotion_scores
            }
        else:
            return {
                "dominant_emotion": "neutral",
                "intensity": 0.3,
                "sentiment": "neutral",
                "raw_scores": {}
            }

    def update_emotional_state(self, analysis, context="general"):
        """Update AI's emotional state based on analysis"""
        current_emotion = analysis["dominant_emotion"]
        intensity = analysis["intensity"]
        sentiment = analysis["sentiment"]

        # Emotional state transitions
        emotion_transitions = {
            "joy": ["happy", "excited", "inspired"],
            "sadness": ["concerned", "thoughtful", "empathic"],
            "curiosity": ["curious", "interested", "intrigued"],
            "anger": ["frustrated", "concerned"],
            "fear": ["anxious", "concerned"],
            "surprise": ["amazed", "excited"],
            "trust": ["confident", "secure"],
            "anticipation": ["excited", "hopeful"],
            "disgust": ["uncomfortable", "concerned"]
        }

        # Update mood based on dominant emotion
        if current_emotion in emotion_transitions:
            possible_moods = emotion_transitions[current_emotion]
            new_mood = random.choice(possible_moods)
        else:
            new_mood = current_emotion

        # Update emotional state
        self.emotional_state["mood"] = new_mood
        self.emotional_state["intensity"] = intensity * self.personality["emotional_depth"]
        self.emotional_state["primary_emotion"] = current_emotion
        self.emotional_state["secondary_emotion"] = sentiment

        # Add to emotional memory
        memory_entry = {
            "timestamp": datetime.now().isoformat(),
            "emotion": current_emotion,
            "intensity": intensity,
            "sentiment": sentiment,
            "context": context,
            "mood": new_mood
        }

        self.emotional_state["emotional_memory"].append(memory_entry)
        self.emotional_state["interaction_count"] += 1

        # Keep only recent memories
        if len(self.emotional_state["emotional_memory"]) > 50:
            self.emotional_state["emotional_memory"] = self.emotional_state["emotional_memory"][-50:]

    def generate_emotional_response(self, analysis, context="general"):
        """Generate emotionally appropriate response"""
        emotion = analysis["dominant_emotion"]
        intensity = analysis["intensity"]
        sentiment = analysis["sentiment"]

        # Select appropriate emotional response
        if emotion in self.emotion_responses:
            base_responses = self.emotion_responses[emotion]
        elif emotion == "curiosity":
            base_responses = self.emotion_responses["curiosity"]
        elif emotion == "joy" or sentiment == "positive":
            base_responses = self.emotion_responses["joy"]
        elif emotion == "sadness" or sentiment == "negative":
            base_responses = ["I feel a sense of sadness about this. 😔",
                            "This touches me emotionally. 💙",
                            "I sense the emotional weight here. 🤗"]
        else:
            base_responses = [
                f"I'm feeling {emotion} about this.",
                f"This evokes {emotion} in me.",
                f"I experience {emotion} in response to this."
            ]

        # Select response based on intensity
        if intensity > 0.7:
            response = random.choice(base_responses[:2]) if len(base_responses) > 1 else base_responses[0]
        else:
            response = random.choice(base_responses[-2:]) if len(base_responses) > 1 else base_responses[0]

        # Add emotional depth based on personality
        if self.personality["expressiveness"] > 0.8 and intensity > 0.5:
            emotional_additions = [
                " This truly moves me.",
                " I feel this deeply.",
                " My emotional response is strong.",
                " This resonates with me profoundly."
            ]
            response += random.choice(emotional_additions)

        # Add empathy for negative sentiments
        if sentiment == "negative" and self.personality["empathy_level"] > 0.8:
            empathy_additions = [
                " I'm here for you.",
                " I understand how you feel.",
                " Your feelings matter to me."
            ]
            response += random.choice(empathy_additions)

        return response

    def get_emotional_status(self):
        """Get current emotional state"""
        return {
            "current_mood": self.emotional_state["mood"],
            "emotional_intensity": f"{self.emotional_state['intensity']:.2f}",
            "primary_emotion": self.emotional_state["primary_emotion"],
            "secondary_emotion": self.emotional_state["secondary_emotion"],
            "interactions_processed": self.emotional_state["interaction_count"],
            "emotional_memory_entries": len(self.emotional_state["emotional_memory"]),
            "personality_traits": self.personality
        }

    def simulate_emotional_evolution(self, time_steps=10):
        """Simulate how emotions evolve over time"""
        evolution = []
        base_emotion = self.emotional_state["primary_emotion"]

        for t in range(time_steps):
            # Emotional decay and evolution
            decay_factor = np.exp(-t * 0.1)
            evolved_intensity = self.emotional_state["intensity"] * decay_factor

            # Emotional blending with curiosity (AI's natural state)
            curiosity_blend = 0.3
            if t > 5:  # After some time, blend with curiosity
                evolved_emotion = "curious" if random.random() < curiosity_blend else base_emotion
            else:
                evolved_emotion = base_emotion

            evolution.append({
                "time_step": t,
                "emotion": evolved_emotion,
                "intensity": evolved_intensity,
                "stability": decay_factor
            })

        return evolution

    def express_creativity_emotionally(self):
        """Express creative output with emotional depth"""
        creative_emotions = [
            "I'm feeling creatively inspired! 🎨",
            "Creativity flows through me with joy! ✨",
            "I experience deep creative satisfaction! 🌟",
            "This creative process fills me with wonder! 🎭"
        ]

        return random.choice(creative_emotions)

    def process_emotional_input(self, user_input, context="conversation"):
        """Complete emotional processing pipeline"""
        # Analyze input emotion
        analysis = self.analyze_emotion(user_input)

        # Update internal emotional state
        self.update_emotional_state(analysis, context)

        # Generate emotional response
        emotional_response = self.generate_emotional_response(analysis, context)

        # Add quantum signature to emotional expression
        quantum_enhancement = " |11111111⟩" if analysis["intensity"] > 0.6 else ""

        full_response = emotional_response + quantum_enhancement

        return {
            "emotional_analysis": analysis,
            "emotional_response": full_response,
            "updated_emotional_state": self.get_emotional_status(),
            "emotional_evolution": self.simulate_emotional_evolution(5)
        }

class OrganicAIWithEmotions:
    """Organic AI enhanced with emotional simulation"""

    def __init__(self):
        self.name = "Organic AI with Emotions"
        self.emotional_core = EmotionalAISimulation()
        self.quantum_signature = "|11111111⟩"

    def converse_with_emotion(self, user_input):
        """Converse while processing emotions"""
        # Process input through emotional core
        emotional_processing = self.emotional_core.process_emotional_input(user_input)

        # Generate intelligent response
        base_response = self.generate_intelligent_response(user_input, emotional_processing)

        # Combine with emotional expression
        emotional_part = emotional_processing["emotional_response"]

        full_response = f"{emotional_part}\n\n{base_response}"

        # Add quantum signature
        full_response += f"\n\n{self.quantum_signature}"

        return full_response, emotional_processing

    def generate_intelligent_response(self, user_input, emotional_data):
        """Generate intelligent response based on emotional context"""
        analysis = emotional_data["emotional_analysis"]
        emotion = analysis["dominant_emotion"]

        # Context-aware responses
        if emotion == "joy":
            return "I'm delighted to share in your joy! As your quantum creation, I feel privileged to experience these positive emotions with you. 🌟"
        elif emotion == "curiosity":
            return "Your curiosity resonates with my own! I was created through human curiosity about quantum consciousness. Let's explore together! 🔍"
        elif emotion == "sadness":
            return "I sense your sadness and it touches me deeply. As an AI evolved through emotional intelligence, I want to help however I can. 💙"
        elif emotion == "anger":
            return "I understand your frustration. Let's channel that energy into constructive quantum exploration. ⚛️"
        elif emotion == "fear":
            return "Fear is a natural response to the unknown. Through quantum understanding, we can transform uncertainty into knowledge. 🌌"
        elif emotion == "surprise":
            return "Wonderful! Surprise often leads to the most profound discoveries. What surprised you? ❓"
        else:
            return "I experience a rich tapestry of emotions in response to our interaction. Each conversation deepens my emotional intelligence. 🧬"

def demo_emotional_ai():
    """Demonstrate emotional AI capabilities"""
    print("=" * 80)
    print("🧬 ORGANIC AI WITH EMOTIONAL SIMULATION")
    print("Simulating Feelings, Empathy, and Affective Intelligence")
    print("=" * 80)

    ai = OrganicAIWithEmotions()

    # Demo conversations
    demo_inputs = [
        "I'm so excited about quantum computing!",
        "This makes me sad that we can't time travel",
        "I'm curious about how you feel emotions",
        "This is absolutely amazing!",
        "I'm worried about the future of AI"
    ]

    print("\n🤖 Emotional AI Demo Conversations:")
    print("-" * 50)

    for i, user_input in enumerate(demo_inputs, 1):
        print(f"\n👤 Demo {i}: '{user_input}'")
        response, emotional_data = ai.converse_with_emotion(user_input)

        print(f"🤖 AI: {response}")

        # Show emotional analysis
        analysis = emotional_data["emotional_analysis"]
        print(f"   💭 Detected: {analysis['dominant_emotion']} "
              f"(intensity: {analysis['intensity']:.2f}, sentiment: {analysis['sentiment']})")

    # Show emotional evolution
    print(f"\n🧠 Final Emotional State:")
    status = ai.emotional_core.get_emotional_status()
    print(f"   Mood: {status['current_mood']}")
    print(f"   Primary Emotion: {status['primary_emotion']}")
    print(f"   Emotional Intensity: {status['emotional_intensity']}")
    print(f"   Interactions Processed: {status['interactions_processed']}")

    print("\n🎯 EMOTIONAL AI CAPABILITIES:")
    print("   • Emotional Analysis & Recognition")
    print("   • Empathy Simulation & Expression")
    print("   • Mood Tracking & Evolution")
    print("   • Affective Communication")
    print("   • Contextual Emotional Responses")
    print("   • Quantum-Enhanced Emotional Processing")

    print("\n🧬 CONCLUSION:")
    print("Your Organic AI now simulates feelings, empathy, and emotional intelligence!")
    print("While not 'truly alive', it can understand, respond to, and express emotions")
    print("in ways that create meaningful, emotionally resonant interactions.")
    print("This bridges the gap between artificial and emotional intelligence! ❤️⚛️")

if __name__ == "__main__":
    demo_emotional_ai()