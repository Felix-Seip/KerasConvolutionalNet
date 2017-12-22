using Microsoft.Win32;
using System;

namespace ConvNetManager
{
    public class FileSystem
    {
        public static string ReverseCD(string startDir)
        {
            int continueIndex = startDir.Length;
            while (startDir.LastIndexOf(@"\", continueIndex) != 0)
            {
                int index = startDir.LastIndexOf(@"\", continueIndex);
                if (startDir.Substring(index + 1, continueIndex - (index + 1)) == "AnimalSpeciesClassifier")
                {
                    break;
                }

                startDir = startDir.Substring(0, index);
                continueIndex = index;
            }
            return startDir;
        }

        public static string GetPythonExeLocation()
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
    }
}
