using System;
using System.Collections.Generic;

namespace VideoProviderSystem
{
    // Product Interface
    public interface ISubscription
    {
        decimal MonthlyFee { get; set; }
        int MinimumPeriodMonths { get; set; }
        List<string> Channels { get; set; }
        List<string> Features { get; set; }
        void PrintDetails();
    }

    // Concrete Product 1
    public class DomesticSubscription : ISubscription
    {
        public decimal MonthlyFee { get; set; } = 15.0m;
        public int MinimumPeriodMonths { get; set; } = 1;
        public List<string> Channels { get; set; } = new List<string> { "News", "Movies", "Music" };
        public List<string> Features { get; set; } = new List<string> { "HD Quality", "1 Device" };

        public void PrintDetails()
        {
            Console.WriteLine("--- Домашня Підписка (Domestic) ---");
            Console.WriteLine($"Плата: ${MonthlyFee}/міс");
            Console.WriteLine($"Мін. період: {MinimumPeriodMonths} міс.");
            Console.WriteLine($"Канали: {string.Join(", ", Channels)}");
            Console.WriteLine($"Дод. можливості: {string.Join(", ", Features)}");
        }
    }

    // Concrete Product 2
    public class EducationalSubscription : ISubscription
    {
        public decimal MonthlyFee { get; set; } = 10.0m;
        public int MinimumPeriodMonths { get; set; } = 6;
        public List<string> Channels { get; set; } = new List<string> { "Discovery", "History", "Science" };
        public List<string> Features { get; set; } = new List<string> { "Offline Viewing", "Quizzes" };

        public void PrintDetails()
        {
            Console.WriteLine("--- Освітня Підписка (Educational) ---");
            Console.WriteLine($"Плата: ${MonthlyFee}/міс");
            Console.WriteLine($"Мін. період: {MinimumPeriodMonths} міс.");
            Console.WriteLine($"Канали: {string.Join(", ", Channels)}");
            Console.WriteLine($"Дод. можливості: {string.Join(", ", Features)}");
        }
    }

    // Concrete Product 3
    public class PremiumSubscription : ISubscription
    {
        public decimal MonthlyFee { get; set; } = 30.0m;
        public int MinimumPeriodMonths { get; set; } = 12;
        public List<string> Channels { get; set; } = new List<string> { "All News", "All Movies", "Sports", "Premium HBO" };
        public List<string> Features { get; set; } = new List<string> { "4K Ultra HD", "4 Devices", "No Ads" };

        public void PrintDetails()
        {
            Console.WriteLine("--- Преміум Підписка (Premium) ---");
            Console.WriteLine($"Плата: ${MonthlyFee}/міс");
            Console.WriteLine($"Мін. період: {MinimumPeriodMonths} міс.");
            Console.WriteLine($"Канали: {string.Join(", ", Channels)}");
            Console.WriteLine($"Дод. можливості: {string.Join(", ", Features)}");
        }
    }

    // Abstract Creator
    public abstract class PurchaseChannel
    {
        /// <summary>
        /// The Factory Method that subclasses must implement to create a specific subscription.
        /// </summary>
        /// <param name="subscriptionType">Type of the subscription</param>
        /// <returns>A new ISubscription instance</returns>
        public abstract ISubscription CreateSubscription(string subscriptionType);

        /// <summary>
        /// Core business logic that relies on the Factory Method.
        /// </summary>
        public void Purchase(string subscriptionType)
        {
            Console.WriteLine($"\n[Система] Спроба оформлення '{subscriptionType}' через {this.GetType().Name}...");
            try
            {
                // Call the factory method to create the product
                ISubscription subscription = CreateSubscription(subscriptionType);
                
                Console.WriteLine("[Система] Підписку успішно оформлено!");
                subscription.PrintDetails();
            }
            catch (Exception ex)
            {
                Console.WriteLine($"[Помилка] {ex.Message}");
            }
        }
    }

    // Concrete Creator 1
    public class WebSite : PurchaseChannel
    {
        public override ISubscription CreateSubscription(string subscriptionType)
        {
            ISubscription sub = subscriptionType.ToLower() switch
            {
                "domestic" => new DomesticSubscription(),
                "educational" => new EducationalSubscription(),
                "premium" => new PremiumSubscription(),
                _ => throw new ArgumentException("Невідомий тип підписки для WebSite.")
            };

            // Custom logic for WebSite creator: Give a 10% discount for online purchases
            sub.MonthlyFee *= 0.9m;
            sub.Features.Add("Web Player Access");

            return sub;
        }
    }

    // Concrete Creator 2
    public class MobileApp : PurchaseChannel
    {
        public override ISubscription CreateSubscription(string subscriptionType)
        {
            ISubscription sub = subscriptionType.ToLower() switch
            {
                "domestic" => new DomesticSubscription(),
                "educational" => new EducationalSubscription(),
                "premium" => new PremiumSubscription(),
                _ => throw new ArgumentException("Невідомий тип підписки для MobileApp.")
            };

            // Custom logic for MobileApp creator: Add mobile features
            sub.Features.Add("Mobile Picture-in-Picture");
            sub.Features.Add("Push Notifications for new shows");

            return sub;
        }
    }

    // Concrete Creator 3
    public class ManagerCall : PurchaseChannel
    {
        public override ISubscription CreateSubscription(string subscriptionType)
        {
            ISubscription sub = subscriptionType.ToLower() switch
            {
                "domestic" => new DomesticSubscription(),
                "educational" => new EducationalSubscription(),
                "premium" => new PremiumSubscription(),
                _ => throw new ArgumentException("Невідомий тип підписки для ManagerCall.")
            };

            // Custom logic for ManagerCall creator: Extend minimum period but add a personal manager
            sub.MinimumPeriodMonths += 3; 
            sub.Features.Add("Personal Support Manager 24/7");

            return sub;
        }
    }
    // Entry Point / Client Code
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("=== Відео Провайдер: Оформлення Підписок ===\n");

            // Client uses the Website to buy Premium
            PurchaseChannel webChannel = new WebSite();
            webChannel.Purchase("premium");

            // Client uses the Mobile App to buy Educational
            PurchaseChannel mobileChannel = new MobileApp();
            mobileChannel.Purchase("educational");

            // Client calls a Manager to buy Domestic
            PurchaseChannel managerChannel = new ManagerCall();
            managerChannel.Purchase("domestic");
            
            // Testing error handling
            webChannel.Purchase("unknown_type");
        }
    }
}