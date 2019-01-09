#include <opencv2/opencv.hpp>
#include <iostream>
using namespace std;
using namespace cv;

int main(void)
{
	//Mat image = imread("image.jpg");
	//FileStorage MatFile("MatFile.xml", FileStorage::WRITE);//对xml文件打开写操作
	//MatFile << "image" << image;
	//MatFile.release();//关闭xml文件

	Mat image;
	FileStorage MatFile("MatFile.xml", FileStorage::READ);//对xml文件打开读操作
	MatFile["image"] >> image;
	MatFile.release();//关闭xml文件

	imshow("image", image);
	waitKey(0);

	return 0;
}