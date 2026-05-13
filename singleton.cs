using System;
using System.Threading.Tasks;

namespace SingletonPattern
{
    /// <summary>
    /// Thread-safe Singleton class.
    /// The 'sealed' modifier prevents derivation, ensuring no subclasses can be created 
    /// which might otherwise bypass the private constructor restrictions.
    /// </summary>
    public sealed class Authenticator
    {
        // Static variable that holds the single instance
        private static Authenticator _instance;
        
        // Lock object for thread synchronization
        private static readonly object _lock = new object();
        
        // A unique identifier to prove that all threads use the exact same instance
        public Guid InstanceId { get; private set; }

        /// <summary>
        /// Private constructor ensures that the object cannot be instantiated from outside.
        /// </summary>
        private Authenticator()
        {
            InstanceId = Guid.NewGuid();
            // This line should only be printed ONCE, proving single instantiation
            Console.WriteLine($"\n[Система] --- Створено ЄДИНИЙ екземпляр Authenticator. ID: {InstanceId} ---\n");
        }

        /// <summary>
        /// Global access point to the single instance.
        /// Uses double-checked locking to ensure thread safety without degrading performance.
        /// </summary>
        public static Authenticator Instance
        {
            get
            {
                // First check (no lock) to avoid locking overhead if instance already exists
                if (_instance == null)
                {
                    // Lock to ensure only one thread enters the critical section
                    lock (_lock)
                    {
                        // Second check (with lock) to ensure another thread hasn't created it in the meantime
                        if (_instance == null)
                        {
                            _instance = new Authenticator();
                        }
                    }
                }
                return _instance;
            }
        }

        /// <summary>
        /// A sample business logic method.
        /// </summary>
        /// <param name="username">Name of the user to authenticate</param>
        public void AuthenticateUser(string username)
        {
            Console.WriteLine($"[Аутентифікація] Користувач '{username}' успішно увійшов. (Обробляє екземпляр: {InstanceId})");
        }
    }

    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("=== Тестування патерну Одинак (Singleton) ===");
            Console.WriteLine("Запуск 10 потоків одночасно для перевірки надійності...\n");

            // Simulating multiple threads trying to access the Authenticator at the same time
            Parallel.For(0, 10, i =>
            {
                // Each thread requests the Singleton instance
                Authenticator auth = Authenticator.Instance;
                
                // Perform some action
                auth.AuthenticateUser($"User_{i}");
            });

            Console.WriteLine("\nТестування завершено. Як бачимо, екземпляр класу був створений лише один раз.");
        }
    }
}