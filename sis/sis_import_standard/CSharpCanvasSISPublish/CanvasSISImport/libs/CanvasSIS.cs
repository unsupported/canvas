using System;
using System.Net;
using System.IO;
using System.Collections;
using Procurios.Public;
using System.Collections.Specialized;
using System.Text;

namespace canvasSIS
{
	public class CanvasSIS
	{
		//public CanvasSIS (){}
		
		private string _account_id = null;
		public string account_id
		{
			set { this._account_id = value; }
			get { return this._account_id; }
		}
		private string _sub_domain = null;
		public string sub_domain
		{
			set { this._sub_domain = value; }
			get { return this._sub_domain; }
		}
		
		private string _access_token = null;
		public string access_token
		{
			set { this._access_token = value; }
			get { return this._access_token; }
		}
		
		
		
		private bool validateSettings(){
			if(access_token!= null && account_id != null && sub_domain != null){
				return true;
			}else{
				return false;	
			}
		}
		public Hashtable PostCanvasSISImport(string filename, string extension){
			if(!validateSettings()){
				// TODO I know null isn't the best response for this return type but if the settings aren't valid it shouldn't
				// work.  What is a better return type?
				return null;
			}else{
				string url = @"https://" + sub_domain + ".instructure.com/api/v1/accounts/"+account_id+"/sis_imports.json";
				
				NameValueCollection nvc = new NameValueCollection();
				
				nvc.Add("import_type","instructure_csv");
				nvc.Add("access_token",access_token);
				nvc.Add("extension",extension);
				
	          	WebClient client = new WebClient(); 
				client.QueryString = nvc;
				
				client.Headers.Add("Content-Type","application/x-www-form-urlencoded");
				
				byte[] fileContents = System.IO.File.ReadAllBytes(filename);
				
				byte[] responseBinary = client.UploadData(url,"POST",fileContents);
				
				string response = Encoding.UTF8.GetString(responseBinary);	
				
				
				Console.WriteLine("response: " + response);
				// return response;
				Hashtable json_response = returnJson(response);
				json_response["raw_response"] = response;
				return json_response;
			}
		}
		/*
		 * This method can be called without a file extension, but when it does it defaults
		 * to 'csv'.
		 */
		public Hashtable PostCanvasSISImport(string filename)
		{
			 return PostCanvasSISImport(filename,"csv");
		}
		
		public Hashtable CheckStatus(String sis_import_id)
		{
			//string url = @"https://" + sub_domain + ".instructure.com/api/v1/accounts/82726/sis_imports/"+sis_import_id +".json?access_token=<access_token>";
            string url = @"https://" + sub_domain + ".instructure.com/api/v1/accounts/"+account_id+"/sis_imports/"+sis_import_id+".json?access_token="+access_token;
           	
           	NameValueCollection nvc = new NameValueCollection();
			
			nvc.Add("access_token",access_token);
			WebClient client = new WebClient(); 
			client.QueryString = nvc;
			byte[] responseBinary = client.DownloadData(url);
			string response = Encoding.UTF8.GetString(responseBinary);
			
			//return response;
			Hashtable json_response = returnJson(response);
			json_response["raw_response"] = response;
			return json_response;
			
		}
		

		private Hashtable returnJson(string s){
			Hashtable o;
			//bool success = true;
			o = (Hashtable)JSON.JsonDecode(s);	
			//Console.WriteLine (o["id"]);
			return o;
		}
		
		
	}
}

