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
            server.WaitForConnection();

            stream = new MemoryStream();
            writer = new BinaryWriter(stream);
            StartConvNetScript();
        }

        private void StartConvNetScript()
        {
            ProcessStartInfo start = new ProcessStartInfo();
            start.FileName = "  my/full/path/to/python.exe";
            start.Arguments = string.Format("{0} {1}", cmd, args);
            start.UseShellExecute = false;
            start.RedirectStandardOutput = true;
            Process process = Process.Start(start);
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
            writer.Write(random.Next() + "");
            server.Write(stream.ToArray(), 0, stream.ToArray().Length);
            GetResponseAsync();
        }
    }
}
