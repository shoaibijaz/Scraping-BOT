using Selenium;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace DarazExtractor
{
    public partial class Form2 : Form
    {
        public Form2()
        {
            InitializeComponent();
        }

        private ISelenium selenium;

        public string checkVersion()
        {
            OperatingSystem OS = Environment.OSVersion;
            string OSDetails = OS.VersionString;
            return OSDetails;
        }

        public void SetupStart()
        {
            if (checkVersion() == "Microsoft Windows NT 6.1.7601 Service Pack 1")
            {
                selenium = new DefaultSelenium("localhost", 4444, "*firefox C:/Program Files (x86)/Mozilla Firefox/firefox.exe", "https://www.daraz.pk/");
            }
            else
            {
                selenium = new DefaultSelenium("localhost", 4444, "*firefox C:/Program Files/Mozilla Firefox/firefox.exe", "https://www.daraz.pk/");
            }

            selenium.Start();
        }

        public void SetupStop()
        {
            try
            {
                selenium.Stop();
            }
            catch (Exception)
            {
                // Ignore errors if unable to close the browser
                selenium.Close();
            }
        }

        private void Form2_Load(object sender, EventArgs e)
        {

        }

        private void button1_Click(object sender, EventArgs e)
        {
            SetupStart();

            Extract();

        }

        public void Extract()
        {

            selenium.WindowMaximize();

            selenium.SetTimeout("120000");

            selenium.Open("https://www.gumtree.sg/");

            selenium.WaitForPageToLoad("30000");

            if (selenium.IsElementPresent("//*[@id='flexLftBuckt']/li[1]/ul/li[4]/a"))
            {
                selenium.Click("//*[@id='flexLftBuckt']/li[1]/ul/li[4]/a");
                selenium.WaitForPageToLoad("30000");

                var countsList = selenium.GetXpathCount("//li[contains(@class,'result pictures')]");

                for (var i = 1; i <= countsList; i++)
                {
                    var productXPath = "//li[contains(@class,'result pictures')][" + i + "]";

                    if (selenium.IsElementPresent(productXPath)) {
                        var img = selenium.GetAttribute(productXPath + "/div/div[@class='thumb shrtHght']/div/img[1]@src");
                        var title = selenium.GetText("/div/div[@class='container']/div[@class='title']/a");

                        var row = dataGridView1.Rows.Add(dataGridView1.Rows.Count + 1);

                        dataGridView1.Rows[row].Cells[0].Value = img;

                    }

                    
                }
            }

            SetupStop();

        }
    }

    class Products {
        public string Title { get; set; }
    }
}
