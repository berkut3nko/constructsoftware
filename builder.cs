using System;
using System.Collections.Generic;

namespace BuilderPattern
{
    /// <summary>
    /// The complex object that will be built.
    /// Represents a game character (Hero or Enemy).
    /// </summary>
    public class Character
    {
        public string Name { get; set; }
        public int Height { get; set; }
        public string BodyBuild { get; set; }
        public string HairColor { get; set; }
        public string EyeColor { get; set; }
        public string Clothing { get; set; }
        public string CharacterType { get; set; } // "Hero" or "Enemy"
        
        public List<string> Inventory { get; set; } = new List<string>();
        public List<string> Deeds { get; set; } = new List<string>();

        /// <summary>
        /// Prints the fully constructed character's details to the console.
        /// </summary>
        public void PrintStatus()
        {
            Console.WriteLine($"\n=== {CharacterType}: {Name} ===");
            Console.WriteLine($"Зріст: {Height} см | Статура: {BodyBuild}");
            Console.WriteLine($"Колір волосся: {HairColor} | Очі: {EyeColor}");
            Console.WriteLine($"Одяг: {Clothing}");
            Console.WriteLine("Інвентар:");
            foreach (var item in Inventory)
            {
                Console.WriteLine($" - {item}");
            }
            Console.WriteLine("Справи:");
            foreach (var deed in Deeds)
            {
                Console.WriteLine($" * {deed}");
            }
            Console.WriteLine("============================\n");
        }
    }

    /// <summary>
    /// Generic Builder interface for a fluent API.
    /// The generic parameter T allows returning the specific builder type 
    /// (HeroBuilder or EnemyBuilder) to chain specific methods cleanly.
    /// </summary>
    public interface ICharacterBuilder<T> where T : ICharacterBuilder<T>
    {
        T SetName(string name);
        T SetHeight(int heightCm);
        T SetBodyBuild(string build);
        T SetHairColor(string hairColor);
        T SetEyeColor(string eyeColor);
        T SetClothing(string clothing);
        T AddInventoryItem(string item);
        Character Build();
    }

    /// <summary>
    /// Concrete Builder for Hero characters.
    /// Implements the fluent interface and adds specific methods for good deeds.
    /// </summary>
    public class HeroBuilder : ICharacterBuilder<HeroBuilder>
    {
        private Character _character = new Character { CharacterType = "Герой" };

        public HeroBuilder SetName(string name) { _character.Name = name; return this; }
        public HeroBuilder SetHeight(int heightCm) { _character.Height = heightCm; return this; }
        public HeroBuilder SetBodyBuild(string build) { _character.BodyBuild = build; return this; }
        public HeroBuilder SetHairColor(string hairColor) { _character.HairColor = hairColor; return this; }
        public HeroBuilder SetEyeColor(string eyeColor) { _character.EyeColor = eyeColor; return this; }
        public HeroBuilder SetClothing(string clothing) { _character.Clothing = clothing; return this; }
        public HeroBuilder AddInventoryItem(string item) { _character.Inventory.Add(item); return this; }

        /// <summary>
        /// Specific method only available to HeroBuilder.
        /// </summary>
        public HeroBuilder AddGoodDeed(string deed)
        {
            _character.Deeds.Add($"[Добро] {deed}");
            return this;
        }

        public Character Build()
        {
            // Reset state for potential subsequent builds (optional depending on requirements)
            Character builtCharacter = _character;
            _character = new Character { CharacterType = "Герой" };
            return builtCharacter;
        }
    }

    /// <summary>
    /// Concrete Builder for Enemy characters.
    /// Implements the fluent interface and adds specific methods for evil deeds.
    /// </summary>
    public class EnemyBuilder : ICharacterBuilder<EnemyBuilder>
    {
        private Character _character = new Character { CharacterType = "Ворог" };

        public EnemyBuilder SetName(string name) { _character.Name = name; return this; }
        public EnemyBuilder SetHeight(int heightCm) { _character.Height = heightCm; return this; }
        public EnemyBuilder SetBodyBuild(string build) { _character.BodyBuild = build; return this; }
        public EnemyBuilder SetHairColor(string hairColor) { _character.HairColor = hairColor; return this; }
        public EnemyBuilder SetEyeColor(string eyeColor) { _character.EyeColor = eyeColor; return this; }
        public EnemyBuilder SetClothing(string clothing) { _character.Clothing = clothing; return this; }
        public EnemyBuilder AddInventoryItem(string item) { _character.Inventory.Add(item); return this; }

        /// <summary>
        /// Specific method only available to EnemyBuilder.
        /// </summary>
        public EnemyBuilder AddEvilDeed(string deed)
        {
            _character.Deeds.Add($"[Зло] {deed}");
            return this;
        }

        public Character Build()
        {
            Character builtCharacter = _character;
            _character = new Character { CharacterType = "Ворог" };
            return builtCharacter;
        }
    }

    /// <summary>
    /// The Director class defines the order of building steps for predefined characters.
    /// It works with both HeroBuilder and EnemyBuilder using their fluent APIs.
    /// </summary>
    public class CharacterDirector
    {
        /// <summary>
        /// Constructs a predefined dream hero.
        /// </summary>
        public Character ConstructDreamHero(HeroBuilder builder)
        {
            return builder
                .SetName("Елара Світлоносна")
                .SetHeight(175)
                .SetBodyBuild("Спортивна")
                .SetHairColor("Золотисте")
                .SetEyeColor("Смарагдові")
                .SetClothing("Міфрилові обладунки з білим плащем")
                .AddInventoryItem("Святий меч Рассвєт")
                .AddInventoryItem("Зілля лікування")
                .AddGoodDeed("Врятувала сиріт із палаючої будівлі")
                .AddGoodDeed("Перемогла корупцію в магічній раді")
                .Build();
        }

        /// <summary>
        /// Constructs a predefined ultimate nemesis.
        /// </summary>
        public Character ConstructUltimateNemesis(EnemyBuilder builder)
        {
            return builder
                .SetName("Малакар Тіньовий")
                .SetHeight(210)
                .SetBodyBuild("Масивна, залякуюча")
                .SetHairColor("Лисий")
                .SetEyeColor("Палаючі червоні")
                .SetClothing("Мантія зіткана з темряви")
                .AddInventoryItem("Проклятий посох душ")
                .AddInventoryItem("Отруєний кинджал")
                .AddEvilDeed("Затьмарив сонце над королівством")
                .AddEvilDeed("Вкрав останнє печиво у дитини")
                .Build();
        }
    }

    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("=== Тестування патерну Будівельник (Builder) з Fluent Interface ===");

            CharacterDirector director = new CharacterDirector();

            // 1. Building the Dream Hero using Director
            HeroBuilder heroBuilder = new HeroBuilder();
            Character dreamHero = director.ConstructDreamHero(heroBuilder);
            dreamHero.PrintStatus();

            // 2. Building the Nemesis using Director
            EnemyBuilder enemyBuilder = new EnemyBuilder();
            Character nemesis = director.ConstructUltimateNemesis(enemyBuilder);
            nemesis.PrintStatus();

            // 3. Building a custom character on the fly using Fluent Interface directly (without Director)
            Console.WriteLine("--- Створення кастомного персонажа без Директора ---");
            Character customRogue = new HeroBuilder()
                .SetName("Флінн Швидкі Руки")
                .SetHeight(180)
                .SetBodyBuild("Худорлява")
                .SetHairColor("Темне")
                .SetEyeColor("Карі")
                .SetClothing("Шкіряна броня та каптур")
                .AddInventoryItem("Відмички")
                .AddInventoryItem("Димова шашка")
                .AddGoodDeed("Повернув вкрадений гаманець (після того як сам його вкрав)")
                .Build();
            
            customRogue.PrintStatus();
        }
    }
}