using System;
using System.Collections.Generic;

namespace PrototypePattern
{
    /// <summary>
    /// Prototype interface declaring the clone method.
    /// </summary>
    public interface IVirusPrototype
    {
        Virus Clone();
    }

    /// <summary>
    /// Concrete prototype representing a Virus.
    /// </summary>
    public class Virus : IVirusPrototype
    {
        public double Weight { get; set; }
        public int Age { get; set; }
        public string Name { get; set; }
        public string Species { get; set; }
        
        // Array/List of children, which are also Virus instances
        public List<Virus> Children { get; set; }

        public Virus(double weight, int age, string name, string species)
        {
            Weight = weight;
            Age = age;
            Name = name;
            Species = species;
            Children = new List<Virus>();
        }

        /// <summary>
        /// Implements a deep copy of the Virus and all its descendants.
        /// </summary>
        /// <returns>A fully independent clone of the original Virus.</returns>
        public Virus Clone()
        {
            // Create a new instance with copied primitive values and strings
            Virus clonedVirus = new Virus(this.Weight, this.Age, this.Name, this.Species);
            
            // Deep copy the children array/list recursively
            foreach (var child in this.Children)
            {
                clonedVirus.Children.Add(child.Clone());
            }

            return clonedVirus;
        }

        /// <summary>
        /// Helper method to visually print the family tree of the virus.
        /// </summary>
        public void PrintStatus(string prefix = "")
        {
            Console.WriteLine($"{prefix}Вірус: {Name} | Вид: {Species} | Вага: {Weight} | Вік: {Age} | К-ть дітей: {Children.Count}");
            
            // Recursively print children with an indented prefix
            foreach (var child in Children)
            {
                child.PrintStatus(prefix + "  ");
            }
        }
    }

    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("=== Тестування патерну Прототип (Prototype) ===\n");

            // 1. Generation 3 (Grandchildren)
            Virus child1 = new Virus(0.5, 1, "Вірус-Онук-1", "COVID-19");
            Virus child2 = new Virus(0.6, 1, "Вірус-Онук-2", "COVID-19");

            // 2. Generation 2 (Children)
            Virus parent1 = new Virus(1.2, 5, "Вірус-Син-1", "COVID-19");
            parent1.Children.Add(child1); // Adding 3rd generation to 2nd
            parent1.Children.Add(child2);

            Virus parent2 = new Virus(1.1, 4, "Вірус-Донька-1", "COVID-19");

            // 3. Generation 1 (Grandparent / Root)
            Virus grandparent = new Virus(2.5, 10, "Вірус-Батько", "COVID-19");
            grandparent.Children.Add(parent1); // Adding 2nd generation to 1st
            grandparent.Children.Add(parent2);

            Console.WriteLine("--- Оригінальне сімейство вірусів ---");
            grandparent.PrintStatus();

            // 4. Cloning the root virus
            Console.WriteLine("\n--- Клонування віруса-батька ---");
            Virus clonedGrandparent = grandparent.Clone();
            
            // 5. Modifying the clone to prove deep copy works correctly
            clonedGrandparent.Name = "Вірус-Клон-Батько";
            clonedGrandparent.Children[0].Name = "Вірус-Клон-Син-1"; // Modifying Gen 2
            clonedGrandparent.Children[0].Children[0].Name = "Вірус-Клон-Онук-1"; // Modifying Gen 3
            clonedGrandparent.Children[0].Children[0].Weight = 99.9; 

            Console.WriteLine("\n--- Клоноване сімейство після модифікацій ---");
            clonedGrandparent.PrintStatus();

            Console.WriteLine("\n--- Оригінальне сімейство (має залишитись без змін) ---");
            grandparent.PrintStatus();
            
            Console.WriteLine("\nТестування завершено. Глибоке копіювання (Deep Copy) працює коректно.");
        }
    }
}