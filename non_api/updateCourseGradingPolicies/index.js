const fs = require("fs-extra");
const request = require("request-promise");
const async = require("async");
const path = require("path");
const _ = require("underscore");
const puppeteer = require("puppeteer");

/***           Canvas Webcrawler 
            
Crawls through each course on your canvas site that you 
list and then switches on the manual grading posting
policy for each course.
Written in NodeJS by Robert Payne (rpaynelms@gmail.com)
Working as of 03/03/2020

Remember to run 'npm install' before running this script ('node index.js')

    HEADLESS BRROWSING VARIABLES      **/
const siteBase = "https://YOURSITE.instructure.com";
const userName = "USERNAME";
const pass = "PASSWORD";
const headlessBool = false; //false if you want to watch, true if you don't
var courseList = ["course1","course2","course3","course4","course5","course6","course7"] //sis ids for all courses you want to update

crawl(); //it begins
async function crawl() {
	const loginP = siteBase + "/login/canvas/";
	const browser = await puppeteer.launch({ headless: headlessBool });//Start headless browser
	const page = await browser.newPage();
	await page.setViewport({width:2000,height:1200});
	
	//Login
    await page.goto(loginP); 
    await page.type("#pseudonym_session_unique_id", userName);
    await page.type("#pseudonym_session_password", pass);
	await page.click(".Button");
	
	//Go through the courses
	for(var course in courseList){ 
		console.log(courseList[course]);
		await page.goto(siteBase+"/courses/sis_course_id:"+courseList[course]+"/gradebook", {waitUntil: 'networkidle0',});
		await page.click("#gradebook-settings-button");
		await page.waitFor(1000);
		await page.click("[role='tab']:nth-child(2)");
		await page.waitFor(2000);
		await page.click('#GradePostingPolicyTabPanel__PostManually');
		await page.waitFor(2000);
		await page.click('#gradebook-settings-update-button');	
		await page.waitFor(4000);		
	}
	
	await browser.close();
}