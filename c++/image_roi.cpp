#include <opencv2\opencv.hpp>
#include <fstream>
#include <iostream>
using namespace cv;
using namespace std;

string RightPath = "./images-raccoon/";

int CountLines(string& filename)
{
	ifstream ReadFile;
	int n = 0;
	char line[512];
	ReadFile.open(filename.c_str(), ios::in);//ios::in 表示以只读的方式读取文件
	if (ReadFile.fail())//文件打开失败:返回0
	{
		return 0;
	}
	else//文件存在
	{
		while (!ReadFile.eof())
		{
			ReadFile.getline(line, 512, '\n');
			n++;
		}
		return n;
	}

	ReadFile.close();
}

int main(void)
{
	Mat src, temp;
	string ImagesName;//文件名

	int RightNum = (CountLines(RightPath + "img.txt") - 1);

	cout << "RightNum = " << RightNum << '\t' << endl;

	Range RIOy(44, 381);
	Range RIOx(92, 499);

	ifstream finPos(RightPath + "img.txt");
	for (int num = 0; num < RightNum && getline(finPos, ImagesName); num++)
	{
		ImagesName = RightPath + ImagesName;
		cout << ImagesName << endl;
		src = imread(ImagesName);
		temp = src(RIOy, RIOx);//设置RIO
		ImagesName = RightPath + "000-" + to_string(num) + ".jpg";
		imwrite(ImagesName, temp);
	}
	finPos.close();

	return 0;
}