using System;
using System.Collections;
using canvasSIS;
using System.Threading;

namespace CanvasSISApplication
{
    class Program
    {
        static void Main(string[] args)
        {
			CanvasSIS sis = new CanvasSIS();
            // Replace this with you own access token.  
			sis.access_token = "h3xyPlREWirj4FDjJTzakHga6j6YEBo7AoOfvSQW";
            // Same here with the account ID.  You can get this in the URL when you are viewing your account settings.
            // i.e. http://cwt.instructure.com/acccounts/8276 8276 is the account id.
			sis.account_id = "8276";
            // replace this with your subdomain.  i.e. the part before instructure.com
			sis.sub_domain = "cwt";
            // Put the FULL PATH to the file you will be importing.  
            Hashtable post_results = sis.PostCanvasSISImport(@"C:\Users\kevin\Desktop\test_exe\sis_folders\courses.zip", "zip");

            // --------------- End configuration changes

            //Console.WriteLine(post_results.Keys.ToString());
            Console.WriteLine("id: " + post_results["id"]);

            // sis_import_id will represent the id of the queued sis import.  It is used
            // later to check the status of the sis import
            string sis_import_id = post_results["id"].ToString();


            Hashtable status;
			
			ArrayList processingStatuses = new ArrayList();
			
			processingStatuses.Add ("created");
			processingStatuses.Add ("importing");
            Console.WriteLine("waiting for the import to finish....");
            do
            {
                status = sis.CheckStatus(sis_import_id);

                // Uncomment the next line to see the raw api response output on the console.
                //Console.WriteLine(status["raw_response"]);
                // Console.WriteLine("status: " + status["workflow_state"]);

                // TODO Does this really need to sleep? I guess so if we don't want to hit the (unpublished) API limits to quickly.
				Thread.Sleep(2000);
            } while (processingStatuses.Contains((string)status["workflow_state"]));

            Console.WriteLine("All done with status: " + status["workflow_state"]);


        }
    }
}