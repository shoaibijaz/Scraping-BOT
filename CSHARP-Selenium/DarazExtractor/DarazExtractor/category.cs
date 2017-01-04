using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DarazExtractor
{
    public class Category
    {
        public string name { get; set; }
        public string parent { get; set; }
        public string url { get; set; }


        public void Extract()
        {
            var jsonText = System.IO.File.ReadAllText("data.json");

            var categories = Newtonsoft.Json.JsonConvert.DeserializeObject<List<Category>>(jsonText);

            var parent = categories.Where(c => string.IsNullOrEmpty(c.parent));

            var newCategories = new List<Category>();

            foreach (var item in parent)
            {
                var child = categories.Where(c => c.parent.Trim() == item.name.Trim());

                if (child.Any())
                {
                    foreach (var c2 in child)
                    {
                        var c2_child = categories.Where(c => c.parent.Trim() == c2.name.Trim()).ToList();

                        if (c2_child.Any())
                        {
                            c2_child.Where(c => c.url != "https://www.daraz.pk/#").ToList().ForEach(c => newCategories.Add(c));
                        }
                        else if (c2.url != "https://www.daraz.pk/#")
                        {
                            newCategories.Add(c2);
                        }
                    }
                }
                else if (item.url != "https://www.daraz.pk/#")
                {
                    newCategories.Add(item);
                }
            }

            var json = Newtonsoft.Json.JsonConvert.SerializeObject(newCategories);

            File.WriteAllText("data-cl.json",json);

        }
    }
}
