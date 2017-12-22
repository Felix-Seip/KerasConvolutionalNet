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
            server = new NamedPipeServerStream("Demo");
            stream = new MemoryStream();
            writer = new BinaryWriter(stream);
        }

        private void StartConvNetScript()
        {
            string curDir = Directory.GetCurrentDirectory();
            curDir = FileSystem.ReverseCD(curDir);

            ProcessStartInfo start = new ProcessStartInfo();
            start.FileName = FileSystem.GetPythonExeLocation();
            start.Arguments = string.Format("{0} {1} {2} {3}", curDir + @"\AnimalSpeciesClassifier\CNNLauncher.py", "N", @"C:\Users\SeipF\Documents\pokemon_dataset\training", @"C:\Users\SeipF\Documents\pokemon_dataset\test");
            start.UseShellExecute = false;
            start.RedirectStandardOutput = false;
            Process process = Process.Start(start);
        }

        private async void GetResponseAsync()
        {
            byte[] responseBytes = new byte[1028];
            await server.ReadAsync(responseBytes, 0, responseBytes.Length);
            string responseString = Encoding.UTF8.GetString(responseBytes);
            string response = responseString.Substring(0, responseString.IndexOf("\0"));
            ProcessResponse(response);
        }

        private void ProcessResponse(string response)
        {
            string[] responseType = response.Split(':');
            if(responseType[0] == "Status")
            {
                ConnectionStatus.Content = responseType[1];
            }
        }

        //Use this to send a message to the script
        //writer.Write(input.Text);
        //server.Write(stream.ToArray(), 0, stream.ToArray().Length);

        private void Button_Click(object sender, RoutedEventArgs e)
        {
            StartConvNetScript();
            server.WaitForConnection();
            GetResponseAsync();
        }
    }
}
