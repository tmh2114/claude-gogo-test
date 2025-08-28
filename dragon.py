#!/usr/bin/env python3
"""
Dragon Module - A powerful dragon implementation
"""

import random
from typing import List, Tuple


class Dragon:
    """A majestic dragon with various abilities"""
    
    def __init__(self, name: str = "Pyraxis", element: str = "fire"):
        self.name = name
        self.element = element
        self.health = 1000
        self.power = 150
        self.treasure_hoard = []
        self.is_flying = False
        
    def breathe_attack(self) -> str:
        """Unleash a devastating breath attack"""
        attacks = {
            "fire": "🔥 Scorching flames engulf the area!",
            "ice": "❄️ Freezing blizzard chills everything!",
            "lightning": "⚡ Thunder and lightning strike down!",
            "shadow": "🌑 Darkness consumes all light!"
        }
        return f"{self.name} unleashes: {attacks.get(self.element, attacks['fire'])}"
    
    def fly(self) -> str:
        """Take to the skies"""
        if not self.is_flying:
            self.is_flying = True
            return f"{self.name} spreads mighty wings and soars into the sky! 🐉"
        return f"{self.name} is already airborne, ruling the skies!"
    
    def land(self) -> str:
        """Return to the ground"""
        if self.is_flying:
            self.is_flying = False
            return f"{self.name} descends gracefully, landing with earth-shaking power!"
        return f"{self.name} is already on the ground."
    
    def add_treasure(self, item: str) -> None:
        """Add to the dragon's hoard"""
        self.treasure_hoard.append(item)
        
    def roar(self) -> str:
        """Let out a mighty roar"""
        return f"ROOOOAAAAAR! {self.name} shakes the earth with a deafening roar! 🐲"
    
    def display_stats(self) -> str:
        """Show dragon statistics"""
        stats = f"""
╔══════════════════════════════════╗
║       DRAGON: {self.name.upper():^16} ║
╠══════════════════════════════════╣
║ Element: {self.element:^23} ║
║ Health:  {self.health:^23} ║
║ Power:   {self.power:^23} ║
║ Flying:  {str(self.is_flying):^23} ║
║ Treasure Count: {len(self.treasure_hoard):^15} ║
╚══════════════════════════════════╝
        """
        return stats.strip()


class DragonLair:
    """A lair where dragons dwell"""
    
    def __init__(self, location: str = "Mountain Peak"):
        self.location = location
        self.dragons: List[Dragon] = []
        self.defenses = ["Lava moat", "Enchanted barriers", "Guardian spirits"]
        
    def add_dragon(self, dragon: Dragon) -> None:
        """Add a dragon to the lair"""
        self.dragons.append(dragon)
        
    def summon_dragons(self) -> str:
        """Call all dragons to the lair"""
        if not self.dragons:
            return "The lair is empty... no dragons respond to the call."
        
        responses = []
        for dragon in self.dragons:
            responses.append(f"  • {dragon.name} the {dragon.element} dragon arrives!")
        
        return "Dragons answer the summon:\n" + "\n".join(responses)


def create_legendary_dragon() -> Dragon:
    """Create a legendary dragon with random attributes"""
    names = ["Bahamut", "Tiamat", "Smaug", "Drogon", "Viserion", "Alduin"]
    elements = ["fire", "ice", "lightning", "shadow"]
    
    dragon = Dragon(
        name=random.choice(names),
        element=random.choice(elements)
    )
    
    # Legendary dragons are more powerful
    dragon.health = 2500
    dragon.power = 350
    
    # Give them some starting treasure
    treasures = ["Golden Crown", "Magic Orb", "Ancient Sword", "Phoenix Feather"]
    for _ in range(3):
        dragon.add_treasure(random.choice(treasures))
    
    return dragon


def dragon_battle(dragon1: Dragon, dragon2: Dragon) -> str:
    """Simulate an epic dragon battle"""
    result = f"""
⚔️ EPIC DRAGON BATTLE ⚔️
{dragon1.name} ({dragon1.element}) VS {dragon2.name} ({dragon2.element})

Round 1: {dragon1.name} strikes with {dragon1.breathe_attack()}
Round 2: {dragon2.name} counters with {dragon2.breathe_attack()}
Round 3: Both dragons take to the skies!

The battle rages on...
    """
    
    winner = dragon1 if dragon1.power > dragon2.power else dragon2
    result += f"\nVictor: {winner.name} emerges triumphant! 👑"
    
    return result


# Example usage
if __name__ == "__main__":
    print("🐉 Welcome to the Dragon Realm! 🐉\n")
    
    # Create a fire dragon
    fire_dragon = Dragon("Ignis", "fire")
    print(fire_dragon.display_stats())
    print()
    
    # Dragon actions
    print(fire_dragon.roar())
    print(fire_dragon.fly())
    print(fire_dragon.breathe_attack())
    print()
    
    # Create a lair
    lair = DragonLair("Volcanic Fortress")
    lair.add_dragon(fire_dragon)
    
    # Add a legendary dragon
    legendary = create_legendary_dragon()
    lair.add_dragon(legendary)
    
    print(lair.summon_dragons())
    print()
    
    # Dragon battle!
    print(dragon_battle(fire_dragon, legendary))