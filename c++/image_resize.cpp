#include <opencv2\opencv.hpp>
#include <fstream>
#include <iostream>
using namespace cv;
using namespace std;

string Path = "./训练集/";//保存文件路径

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
	int LeftNum = (CountLines(Path + "img.txt") - 1);

	ifstream FINPos(Path + "img.txt");
	for (int num = 0; num < LeftNum && getline(FINPos, ImagesName); num++)
	{
		ImagesName = Path + ImagesName;
		cout << ImagesName << endl;
		src = imread(ImagesName);

		resize(src, src, Size(64, 48));

		imwrite(ImagesName, src);
	}
	FINPos.close();

	return 0;
}