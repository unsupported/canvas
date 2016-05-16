package com.kajigga.canvasapi;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.UnsupportedEncodingException;

import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.mime.MultipartEntity;
import org.apache.http.entity.mime.content.FileBody;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.util.EntityUtils;

import com.google.gson.Gson;

@SuppressWarnings("deprecation")
public class ImportSIS {
	private APIConfig api_config;
	public ImportSIS() {
		String default_config = "{ access_token:\"\","
				+ "account_id:\"\","
				+ "domain:\"\","
				+ "filename_to_import:\"\","
				+ "filetype:\"zip\" }";
		readConfigFromString(default_config);
	}

	public int doImport(){
		return doImport(api_config.import_file,api_config.filetype);
	}
	
	public void setDomain(String domain){
		
	}
	
	public int doImport(String filename,String extension){
		HttpClient httpclient = new DefaultHttpClient();
		
		int returnInt = 0;
		try {
			HttpPost httppost = new HttpPost("https://"+api_config.domain+".instructure.com/api/v1/accounts/"+ api_config.account_id+"/sis_imports?"
					+ "import_type=instructure_csv&extension="+extension);
			log("token: " + this.api_config.access_token);
			log("filename to read: " + filename);
			log("extension: " +extension);
			
			httppost.addHeader("Authorization", "Bearer "+this.api_config.access_token);
			FileBody bin = new FileBody(new File(filename));
			
			MultipartEntity reqEntity = new MultipartEntity();
			reqEntity.addPart("attachment", bin);
			
			httppost.setEntity(reqEntity);

			log("executing request " + httppost.getRequestLine());
			HttpResponse response = httpclient.execute(httppost);
			HttpEntity resEntity = response.getEntity();

			log("----------------------------------------");
			log(response.getStatusLine().toString());
			if (resEntity != null) {
				ImportResponse importResponse = ResponseToImportResponse(resEntity.getContent());
				returnInt = importResponse.id;
			}
			EntityUtils.consume(resEntity);
		} catch (UnsupportedEncodingException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (ClientProtocolException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} finally {
			try {
				httpclient.getConnectionManager().shutdown();
			} catch (Exception ignore) {
			}
		}
		return returnInt;
	}
	
	/**
	 * Whereas the method doImport sends data to Canvas, this method can be called to wait for the completion
	 * of the import.
	 * 
	 * To determine how many cycles (1 cycle every 5 seconds)
	 * to wait for, give it a max_wait_cycles greater than 0.  Otherwise, set max_wait_cycles
	 * to 0 to have it go forever.
	 * 
	 * @param importID
	 * @param max_wait_cycles integer 
	 * @return String
	 */

	public String WaitForCompletion(int importID,int max_wait_cycles){
		String status = "done";
		HttpClient client = new DefaultHttpClient();
		HttpGet request = new HttpGet("https://"+api_config.domain+".instructure.com/api/v1/accounts/"+api_config.account_id+"/sis_imports/"+importID);
		request.addHeader("Authorization", "Bearer "+api_config.access_token);
		int progress = 0;
		HttpResponse response;
		int loop_count = 1;
		while(progress < 100){
			try {
				response = client.execute(request);
				ImportResponse ir_json = ResponseToImportResponse(response.getEntity().getContent());
				progress = ir_json.progress;
				// System.out.println("Progress is: "+progress);
			} catch (ClientProtocolException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
			loop_count+=1;
			if(max_wait_cycles == 0 || loop_count <= max_wait_cycles){
				RequestWait.waitABit(5); // Wait 5 seconds before calling this again.				
			}else{
				status = "timed out waiting for completion";
				break;
			}
		}
		return status;
	}
	/**
	 * This method reads the input stream response from the HTTP client request and converts it into a
	 * GSON (JSON) java object
	 * @param inputStream
	 * @return
	 */
	public ImportResponse ResponseToImportResponse(InputStream inputStream){
		String output = "";
		String line = "";
		BufferedReader rd = new BufferedReader(new InputStreamReader( inputStream));
		
		try {
			while ((line = rd.readLine()) != null){
				output+=line;
			}
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		Gson gson = new Gson();
		log(output);
		ImportResponse jsonObject = gson.fromJson(output, ImportResponse.class);
		return jsonObject;
	}
	
	/**
	 * 
	 * Take a string and convert it into an APIConfig GSON Java object
	 * 
	 * @param config_string
	 */
	public void readConfigFromString(String config_string){
		Gson gson = new Gson();
		log(config_string);
		api_config = gson.fromJson(config_string, APIConfig.class); 
	}
	
	/**
	 * This method reads the config file given by the argument filename 
	 * and parses it from json to a Java native object.
	 * @param filename
	 */
	public void readConfigFromFile(String filename){
		
		File file = new File(filename);
		FileInputStream fis = null;
		 
		try {
			fis = new FileInputStream(file);
 
			log("Total file size to read (in bytes) : " + fis.available());
 
			int content;
			String config_content = "";
			while ((content = fis.read()) != -1) {
				// convert to char and display it
				
				config_content += (char) content;
			}		
			readConfigFromString(config_content);
		} catch (IOException e) {
			e.printStackTrace();
		} finally {
			try {
				if (fis != null)
					fis.close();
			} catch (IOException ex) {
				ex.printStackTrace();
			}
		}
	}
	
	/**
	 * Write lines to System.out.  This method might be written to write the lines to a log
	 * file also.
	 * 
	 * @param output_string
	 * @param newline
	 */

	public void log(String output_string){
		System.out.println(output_string);
		// TODO Log this to a file too.
	}
	
}
