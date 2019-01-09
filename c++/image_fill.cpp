#include <opencv2\opencv.hpp>
#include <fstream>
#include <iostream>
using namespace cv;
using namespace std;

string Path = "./images/wrong/";

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
	Mat src;
	string ImagesName;//文件名

	int Num = (CountLines(Path + "img.txt") - 1);
	cout << Num << endl;

	ifstream finPos(Path + "img.txt");
	for (int num = 0; num < Num && getline(finPos, ImagesName); num++)
	{
		ImagesName = Path + ImagesName;
		cout << ImagesName << endl;
		src = imread(ImagesName);
		copyMakeBorder(src, src, 0, 0, 128, 128, BORDER_CONSTANT, Scalar(0, 0, 0));//黑色
		imwrite(ImagesName, src);
	}
	finPos.close();

	return 0;
}