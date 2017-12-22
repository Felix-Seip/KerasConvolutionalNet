using Microsoft.Win32;
using System;
using System.Diagnostics;
using System.IO;
using System.IO.Pipes;
using System.Text;
using System.Windows;

namespace ConvNetManager
{
    /// <summary>
    /// Interaktionslogik für MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        NamedPipeServerStream server;
        MemoryStream stream;
        BinaryWriter writer;
        Random random = new Random();

        public MainWindow()
        {
            InitializeComponent();
            StartConvNetScript();

            server = new NamedPipeServerStream("Demo");
            server.WaitForConnection();

            stream = new MemoryStream();
            writer = new BinaryWriter(stream);
        }

        private void StartConvNetScript()
        {
            string curDir = Directory.GetCurrentDirectory();

            int continueIndex = curDir.Length;
            while (curDir.LastIndexOf(@"\", continueIndex) != 0)
            {
                int index = curDir.LastIndexOf(@"\", continueIndex);
                if (curDir.Substring(index + 1, continueIndex - (index + 1)) == "AnimalSpeciesClassifier")
                {
                    break;
                }

                curDir = curDir.Substring(0, index);
                continueIndex = index;
            }


            ProcessStartInfo start = new ProcessStartInfo();
            start.FileName = GetPythonExeLocation();
            start.Arguments = string.Format("{0} {1} {2} {3}", curDir + @"\AnimalSpeciesClassifier\CNNLauncher.py", "N", @"C:\Users\SeipF\Documents\pokemon_dataset\training", @"C:\Users\SeipF\Documents\pokemon_dataset\test");
            start.UseShellExecute = false;
            start.RedirectStandardOutput = false;
            Process process = Process.Start(start);
        }

        private string GetPythonExeLocation()
        {
            try
            {
                using (RegistryKey key = Registry.CurrentUser.OpenSubKey(@"Software\Python\PythonCore\3.6\InstallPath"))
                {
                    if (key != null)
                    {
                        Object keyValue = key.GetValue("ExecutablePath");
                        if (keyValue != null)
                        {
                            return keyValue.ToString();
                        }
                        else
                        {
                            throw new Exception("Couldnt find Python installation. Is it installed for this user?");
                        }
                    }
                }
            }
            catch (Exception ex)  //just for demonstration...it's always best to handle specific exceptions
            {
                //react appropriately
            }
            return "";
        }

        private async void GetResponseAsync()
        {
            byte[] responseBytes = new byte[1028];
            await server.ReadAsync(responseBytes, 0, responseBytes.Length);
            string responseString = Encoding.UTF8.GetString(responseBytes);

            responseString = responseString.Substring(0, responseString.IndexOf("\0"));
            input.Text = responseString;
        }

        private void Send_Btn_Click(object sender, RoutedEventArgs e)
        {
            writer.Write(input.Text);
            server.Write(stream.ToArray(), 0, stream.ToArray().Length);
            GetResponseAsync();
        }
    }
}
