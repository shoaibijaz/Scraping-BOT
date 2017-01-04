using MySql.Data.MySqlClient;
using Selenium;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace DarazExtractor
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        List<Category> categories;

        private void Form1_Load(object sender, EventArgs e)
        {
            var jsonText = System.IO.File.ReadAllText("data-cl.json");

            categories = Newtonsoft.Json.JsonConvert.DeserializeObject<List<Category>>(jsonText);

            foreach (var item in categories)
            {
                checkedListBox1.Items.Add(item.name);
            }

        }

        private void button1_Click(object sender, EventArgs e)
        {
            if (checkedListBox1.CheckedIndices.Count > 0)
            {
                foreach (var item in checkedListBox1.CheckedIndices)
                {
                    var category = categories[Convert.ToInt32(item)];

                    SetupStart();

                    Extract(category);
                }

            }

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

        public void Extract(Category category)
        {

            selenium.WindowMaximize();

            selenium.SetTimeout("300000");
            selenium.Open(category.url);

            selenium.SetSpeed("100");

            if (selenium.IsTextPresent("Sorry, the page you have requested was not found"))
            {
                SetupStop();
                return;
            }

            int countpage = 1;

            if (selenium.IsElementPresent("//html/body/main/section/section[@class='pagination']/ul/li"))
            {
                countpage = Convert.ToInt16(selenium.GetXpathCount("html/body/main/section/section[@class='pagination']/ul/li"));

                var lastPage = selenium.GetText("//html/body/main/section/section[@class='pagination']/ul/li[" + (countpage - 1) + "]/a");

                int.TryParse(lastPage, out countpage);
            }

            for (int i = 1; i <= countpage; i++)
            {
                selenium.Open(category.url + "/?page=" + i);

                selenium.WaitForPageToLoad("50000");

                extractProducts(category);
            }

            SetupStop();

        }

        private void extractProducts(Category category)
        {
            MySqlConnection conn = new MySqlConnection();
            conn.ConnectionString = System.Configuration.ConfigurationManager.ConnectionStrings["AppConnectionString"].ConnectionString;
            conn.Open();

            var query = "INSERT INTO products (link, name, price, image, ratings,category) VALUES (@link, @name, @price, @image, @ratings,@category)";

            var urlsList = getExtractedURLS(category);

            var height = selenium.GetElementHeight("//html/body");

            if (height > 0)
            {
                int initial = 0;

                for (int i = 0; i <= height; i++)
                {
                    selenium.GetEval(string.Format("window.scrollTo({0},{1})", initial, i));

                    initial = i;

                    i += i + 50;

                    Thread.Sleep(1000);
                }
            }

            if (selenium.IsElementPresent("//html/body/main/section/section[@class='products']"))
            {
                var productsCount = (int)selenium.GetXpathCount("//html/body/main/section/section[@class='products']/div");

                for (var i = 1; i <= productsCount; i++)
                {
                    var productXPath = "//html/body/main/section/section[@class='products']/div[" + i + "]";

                    if (selenium.GetAttribute(productXPath + "@class").Contains("sku -gallery"))
                    {
                        productXPath = productXPath + "/a[1]";

                        var link = selenium.GetAttribute(productXPath + "@href");
                        var name = selenium.GetText(productXPath + "/h2/span[@class='name']");

                        var price = selenium.GetText(productXPath + "/span[@class='price-box']/span[1]/span[2]");

                        var totalRating = "";

                        if (selenium.IsElementPresent(productXPath + "/div[@class='rating-stars']/div[2]"))
                            totalRating = selenium.GetText(productXPath + "/div[@class='rating-stars']/div[2]");

                        var image = selenium.GetAttribute(productXPath + "/div[@class='image-wrapper default-state']/img@src");

                        if (!urlsList.Contains(link))
                            using (MySqlCommand command = new MySqlCommand(query, conn))
                            {
                                command.Parameters.AddWithValue("@link", link);
                                command.Parameters.AddWithValue("@name", name);
                                command.Parameters.AddWithValue("@price", price);
                                command.Parameters.AddWithValue("@image", image);
                                command.Parameters.AddWithValue("@ratings", totalRating);
                                command.Parameters.AddWithValue("@category", category.name);

                                command.ExecuteNonQuery();
                            }
                    }
                }
            }

            conn.Close();

        }

        private List<string> getExtractedURLS(Category category)
        {
            var list = new List<string>();

            var query = "SELECT link from products WHERE category='" + category.name + "'";

            var connString = System.Configuration.ConfigurationManager.ConnectionStrings["AppConnectionString"].ConnectionString;

            using (MySqlConnection conn = new MySqlConnection(connString))
            {

                conn.Open();

                using (MySqlCommand command = new MySqlCommand(query, conn))
                {
                    using (var reader = command.ExecuteReader())
                    {
                        while (reader.Read())
                        {
                            list.Add(reader["link"].ToString());
                        }


                    }
                }

                conn.Close();
            }

            return list;
        }

    }
}
