#include <opencv2\opencv.hpp>
#include <fstream>
#include <iostream>
using namespace cv;
using namespace std;

/***************************************************************************************************************************************
* @描  述：循环读取帧，直到读取帧到为止
* @参  数：VideoCapture& video，视频流对象
Mat& image，储存读取到的图像
* @返回值：none
**************************************************************************************************************************************/
void ReadFrame(VideoCapture& video, Mat& image)
{
	while (!video.read(image))//直到读取到帧
	{
		continue;
	}
}

int main(void)
{
	VideoCapture video(0);
	Mat src;
	int num = 0;
	string Path = "./images/";
	string path_temp;

	while (1)
	{
		ReadFrame(video, src);
		imshow("src", src);

		if (waitKey(1) == ' ')
		{
			num++;
			path_temp = Path + to_string(num) + ".jpg";
			imwrite(path_temp, src);

			cout << path_temp << endl;
		}
	}
}