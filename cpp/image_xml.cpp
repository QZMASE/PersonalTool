#include <opencv2/opencv.hpp>
#include <iostream>
using namespace std;
using namespace cv;

int main(void)
{
	//Mat image = imread("image.jpg");
	//FileStorage MatFile("MatFile.xml", FileStorage::WRITE);//��xml�ļ���д����
	//MatFile << "image" << image;
	//MatFile.release();//�ر�xml�ļ�

	Mat image;
	FileStorage MatFile("MatFile.xml", FileStorage::READ);//��xml�ļ��򿪶�����
	MatFile["image"] >> image;
	MatFile.release();//�ر�xml�ļ�

	imshow("image", image);
	waitKey(0);

	return 0;
}