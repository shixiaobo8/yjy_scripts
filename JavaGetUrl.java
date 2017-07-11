//package climb_data;
import java.util.*;
import java.io.*;
import java.net.URL;
import java.net.URLConnection;

public class JavaGetUrl{
	public  String baseurl = "http://www.widuu.com/archives/";
	private ArrayList<String> urls;
	private ArrayList<String> videourls;
	
	/***
	*   无参构造
	*/
	public JavaGetUrl(){
		
	}
	
	/***
	* 带参构造
	*/
	public JavaGetUrl(String BaseUrl){
			this.baseurl = BaseUrl;
	}
	
	/**
	*  get方法
	*/
	public ArrayList<String> getUrls(){
		return this.urls;
	}
	
	public ArrayList<String> getVideoUrls(){
		return this.videourls;
	}
	
    public String getBaseUrl(){
		return this.baseurl;
	}
	
	/**
	*	set 方法
	*/
	public void setUrls(ArrayList<String> urls){
		this.urls = urls;
	}
	public void setBaseUrl(String baseurl){
		this.baseurl = baseurl;
	}
	public void setVideoUrls(ArrayList<String> videourls){
		this.videourls = videourls;
	}
	
	public static void main(String args[]){
		JavaGetUrl jg = new JavaGetUrl();
		jg.getActiveVideoUrls();
		System.out.print(jg + "\n\r" + jg.baseurl + "\n\r" + jg.urls);
	}
	
	public ArrayList<String> getActiveVideoUrls(){
		//  先获取成员属性urls的值
		String url = "";
		ArrayList<String> urls = new ArrayList<String>();
		// 通过urls 获取 videourls 的值
		ArrayList<String> videourls = new ArrayList<String>();
		System.out.println("正在爬取数据。。。");
		for(int i=1;i<=100;i++){
			for(int j=1;j<1000;j++){
				url = this.baseurl + "/" + i + "/" + j + ".html";
				try {
					URL u = new URL(url);
					URLConnection conn = u.openConnection();
					InputStream in = u.openStream();
					InputStreamReader isr = new InputStreamReader(in);
					BufferedReader bufr = new BufferedReader(isr);
					String str;
					while ((str = bufr.readLine()) != null) {
						if(str.matches("flashvars")){
							System.out.println(url);
							System.out.println(str);
							videourls.add(url);
						}else{
							continue;
						}
					}
					bufr.close();
					isr.close();
					in.close();
				} catch (Exception e) {
					continue;
					//e.printStackTrace();
				}
				urls.add(url);
			}
		}
		this.urls=urls;
		this.videourls=videourls;
		return videourls;
	}
	
	
}