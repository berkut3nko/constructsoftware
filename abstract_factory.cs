using System;

namespace AbstractFactoryPattern
{
    // ==========================================
    // Abstract Products
    // ==========================================

    /// <summary>
    /// Abstract product interface for Laptops
    /// </summary>
    public interface ILaptop
    {
        void ShowDetails();
    }

    /// <summary>
    /// Abstract product interface for Netbooks
    /// </summary>
    public interface INetbook
    {
        void ShowDetails();
    }

    /// <summary>
    /// Abstract product interface for EBooks
    /// </summary>
    public interface IEBook
    {
        void ShowDetails();
    }

    /// <summary>
    /// Abstract product interface for Smartphones
    /// </summary>
    public interface ISmartphone
    {
        void ShowDetails();
    }

    // ==========================================
    // Concrete Products: IProne Family
    // ==========================================

    public class IProneLaptop : ILaptop
    {
        public void ShowDetails() => Console.WriteLine("[IProne] Ноутбук: Висока продуктивність, закрита екосистема.");
    }

    public class IProneNetbook : INetbook
    {
        public void ShowDetails() => Console.WriteLine("[IProne] Нетбук: Компактний, стильний, легкий.");
    }

    public class IProneEBook : IEBook
    {
        public void ShowDetails() => Console.WriteLine("[IProne] Електронна книга: Retina екран для читання.");
    }

    public class IProneSmartphone : ISmartphone
    {
        public void ShowDetails() => Console.WriteLine("[IProne] Смартфон: Преміальний дизайн, відмінна камера.");
    }

    // ==========================================
    // Concrete Products: Kiaomi Family
    // ==========================================

    public class KiaomiLaptop : ILaptop
    {
        public void ShowDetails() => Console.WriteLine("[Kiaomi] Ноутбук: Топ за свої гроші, потужне залізо.");
    }

    public class KiaomiNetbook : INetbook
    {
        public void ShowDetails() => Console.WriteLine("[Kiaomi] Нетбук: Доступний помічник для студентів.");
    }

    public class KiaomiEBook : IEBook
    {
        public void ShowDetails() => Console.WriteLine("[Kiaomi] Електронна книга: E-Ink дисплей, тривала батарея.");
    }

    public class KiaomiSmartphone : ISmartphone
    {
        public void ShowDetails() => Console.WriteLine("[Kiaomi] Смартфон: Народний вибір, швидка зарядка.");
    }

    // ==========================================
    // Concrete Products: Balaxy Family
    // ==========================================

    public class BalaxyLaptop : ILaptop
    {
        public void ShowDetails() => Console.WriteLine("[Balaxy] Ноутбук: Інноваційний екран AMOLED, сенсорне управління.");
    }

    public class BalaxyNetbook : INetbook
    {
        public void ShowDetails() => Console.WriteLine("[Balaxy] Нетбук: Гнучкий форм-фактор.");
    }

    public class BalaxyEBook : IEBook
    {
        public void ShowDetails() => Console.WriteLine("[Balaxy] Електронна книга: Зручна інтеграція з екосистемою.");
    }

    public class BalaxySmartphone : ISmartphone
    {
        public void ShowDetails() => Console.WriteLine("[Balaxy] Смартфон: Складаний екран, найкращий стилус.");
    }

    // ==========================================
    // Abstract Factory
    // ==========================================

    /// <summary>
    /// The Abstract Factory interface declares a set of methods that return different abstract products.
    /// </summary>
    public interface IDeviceFactory
    {
        ILaptop CreateLaptop();
        INetbook CreateNetbook();
        IEBook CreateEBook();
        ISmartphone CreateSmartphone();
    }

    // ==========================================
    // Concrete Factories
    // ==========================================

    /// <summary>
    /// Concrete factory producing IProne devices
    /// </summary>
    public class IProneFactory : IDeviceFactory
    {
        public ILaptop CreateLaptop() => new IProneLaptop();
        public INetbook CreateNetbook() => new IProneNetbook();
        public IEBook CreateEBook() => new IProneEBook();
        public ISmartphone CreateSmartphone() => new IProneSmartphone();
    }

    /// <summary>
    /// Concrete factory producing Kiaomi devices
    /// </summary>
    public class KiaomiFactory : IDeviceFactory
    {
        public ILaptop CreateLaptop() => new KiaomiLaptop();
        public INetbook CreateNetbook() => new KiaomiNetbook();
        public IEBook CreateEBook() => new KiaomiEBook();
        public ISmartphone CreateSmartphone() => new KiaomiSmartphone();
    }

    /// <summary>
    /// Concrete factory producing Balaxy devices
    /// </summary>
    public class BalaxyFactory : IDeviceFactory
    {
        public ILaptop CreateLaptop() => new BalaxyLaptop();
        public INetbook CreateNetbook() => new BalaxyNetbook();
        public IEBook CreateEBook() => new BalaxyEBook();
        public ISmartphone CreateSmartphone() => new BalaxySmartphone();
    }

    // ==========================================
    // Client Code
    // ==========================================

    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("=== Фабрика виробництва техніки (Abstract Factory) ===\n");

            // 1. Producing IProne Devices
            Console.WriteLine("--- Виробництво техніки IProne ---");
            ProduceDevices(new IProneFactory());

            // 2. Producing Kiaomi Devices
            Console.WriteLine("\n--- Виробництво техніки Kiaomi ---");
            ProduceDevices(new KiaomiFactory());

            // 3. Producing Balaxy Devices
            Console.WriteLine("\n--- Виробництво техніки Balaxy ---");
            ProduceDevices(new BalaxyFactory());

            Console.WriteLine("\nВиробництво завершено успішно!");
        }

        /// <summary>
        /// The client code works with factories and products only through abstract types: 
        /// IDeviceFactory and abstract product interfaces.
        /// </summary>
        static void ProduceDevices(IDeviceFactory factory)
        {
            var laptop = factory.CreateLaptop();
            var netbook = factory.CreateNetbook();
            var ebook = factory.CreateEBook();
            var smartphone = factory.CreateSmartphone();

            // Display device information
            laptop.ShowDetails();
            netbook.ShowDetails();
            ebook.ShowDetails();
            smartphone.ShowDetails();
        }
    }
}