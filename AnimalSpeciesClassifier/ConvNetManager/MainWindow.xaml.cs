using System;
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
