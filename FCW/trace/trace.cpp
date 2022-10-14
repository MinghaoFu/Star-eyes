#include <iostream>
#include <fstream>
#include <stdio.h>
#include <string>
#include <math.h>
#include <vector>
#include <time.h>
using namespace std;
#define LperP 1.524
#define DIRE_INI 0
#define SPE_INI 0
#define MAX_SPE 999
#define ONE_FRAME_TIME 0.1708
#define MAX_ID 100
class object
{
public:
    string name;
    int originalPixel_x;
    int originalPixel_y;
    int birdPixel_x;
    int birdPixel_y;
    double distance;
    int pic_num;
    double speed;
    double direction[2];
    int object_id;
    object(const string& label,int ox,int oy,int bx,int by,double dist,int pn)
    {
        name=label;
        originalPixel_x=ox;
        originalPixel_y=oy;
        birdPixel_x=bx;
        birdPixel_y=by;
        distance=dist;
        pic_num = pn;
        speed = SPE_INI;
        direction[0] = 1;
        direction[1] = DIRE_INI;
        object_id=-1;
    }

};
#define labelNum 6
enum labelSet{
    person, bicycle, motorcycle, traffic_light, truck, car
};
vector<object*> frame0;
vector<object*> frame1;
vector<object*> category[2][labelNum];

bool comp(const object *a, const object *b)
{
    return a->pic_num < b->pic_num;
}

int main()
{
    ifstream index_file;
    index_file.open("./share/index.txt");
    int numOfStream;
    index_file >> numOfStream;
    index_file.close();

    fstream infile0,infile1;
    ofstream outfile;
    infile0.open("./share/dist-from_yolo-old"+to_string(numOfStream-1)+".txt");
    infile1.open("./share/dist-from_yolo"+to_string(numOfStream)+".txt");

    //input
    string label;
    int ox,oy,bx,by;
    double dist;
    int id;
    int numOfStream0;
    int numOfStream1;

    double speed;
    double tangent;
    int direction;

    if(numOfStream<2)
    {
        infile0 >> numOfStream0;
        while(infile0 >> label)
        {
            //cout<<"read "<<label<<endl;
            infile0 >> id;
            infile0 >> ox >> oy >> bx >> by >> dist;
            object* optr = new object(label,ox,oy,bx,by,dist,0);
            optr->object_id=id;
            frame0.push_back(optr);
        }
    }
    else//from final{numOfStream}.txt
    {
        infile0 >> numOfStream0;
        while(infile0 >> label)
        {
            //cout<<"read "<<label<<endl;
            infile0 >> id;
            infile0 >> ox >> oy >> bx >> by >> dist;
            infile0 >> speed >> tangent >> direction;
            object* optr = new object(label,ox,oy,bx,by,dist,0);
            optr->object_id=id;
            frame0.push_back(optr);
        }
    }

    infile1 >> numOfStream1;
    while(infile1 >> label)
    {
        infile1 >> id;
        infile1 >> ox >> oy >> bx >> by >> dist;
        object* optr = new object(label,ox,oy,bx,by,dist,1);
        optr->object_id=-1;
        frame1.push_back(optr);
    }


    for(int i=0;i<frame0.size();i++)
    {
        if(frame0[i]->name=="person")
        {
            category[0][person].push_back(frame0[i]);
        }
        else if(frame0[i]->name=="bicycle")
        {
            category[0][bicycle].push_back(frame0[i]);
        }
        else if(frame0[i]->name=="motorcycle")
        {
            category[0][motorcycle].push_back(frame0[i]);
        }
        else if(frame0[i]->name=="traffic_light")
        {
            category[0][traffic_light].push_back(frame0[i]);
        }
        else if(frame0[i]->name=="truck")
        {
            category[0][truck].push_back(frame0[i]);
        }
        else if(frame0[i]->name=="car")
        {
            category[0][car].push_back(frame0[i]);
        }
    }

    for(int i=0;i<frame1.size();i++)
    {
        if(frame1[i]->name=="person")
            category[1][person].push_back(frame1[i]);
        else if(frame1[i]->name=="bicycle")
            category[1][bicycle].push_back(frame1[i]);
        else if(frame1[i]->name=="motorcycle")
            category[1][motorcycle].push_back(frame1[i]);
        else if(frame1[i]->name=="traffic_light")
            category[1][traffic_light].push_back(frame1[i]);
        else if(frame1[i]->name=="truck")
            category[1][truck].push_back(frame1[i]);
        else if(frame1[i]->name=="car")
            category[1][car].push_back(frame1[i]);
    }

    int id_pool[MAX_ID];
    for(int i=0;i<MAX_ID;i++)
        id_pool[i]=1;//available

    for(int i=0;i<labelNum;i++)
    {
        for(int j=0;j<category[1][i].size();j++)//eg.[1][person]
        {
            double derivative=MAX_SPE;
            for(int k=0;k<category[0][i].size();k++)
            {
                double dx = category[1][i][j]->birdPixel_x - category[0][i][k]->birdPixel_x;
                double dy = category[1][i][j]->birdPixel_y - category[0][i][k]->birdPixel_y;
                if(derivative > sqrt(dx*dx+dy*dy) / ONE_FRAME_TIME * 3.6 / 100) {
                    derivative = sqrt(dx*dx+dy*dy) / ONE_FRAME_TIME * 3.6 / 100;
                    category[1][i][j]->speed = derivative;
                    if(dx!=0)
                        category[1][i][j]->direction[0] = dy / dx;//if dx==0 inf
                    
                    category[1][i][j]->object_id = category[0][i][k]->object_id;
                    id_pool[category[0][i][k]->object_id]=0;//unavailable
                    if ((dy < 0 && dx > 0) || (dy < 0 && dx < 0))
                        category[1][i][j]->direction[1] = 1;//forward
                    else category[1][i][j]->direction[1] = -1;//backward
                }
            }
        }
    }

    for(int i=0;i<frame1.size();i++)
    {
        if(frame1[i]->object_id == -1)
        {
            for(int j=0;j<MAX_ID;j++)
            {
                if(id_pool[j]==1)
                {
                    frame1[i]->object_id = j;
                    id_pool[j]=0;
                    break;
                }
            }
        }
    }
    
    //output
    outfile.open("./share/final"+to_string(numOfStream)+".txt");
    outfile << numOfStream << endl;
    for(int i=0;i<frame1.size();i++)
    {
        outfile << frame1[i]->name << " " << frame1[i]->object_id << endl;
        outfile << frame1[i]->originalPixel_x << " "<< frame1[i]->originalPixel_y << endl;
        outfile << frame1[i]->birdPixel_x << " "<< frame1[i]->birdPixel_y << endl;
        outfile << frame1[i]->distance << endl;
        outfile << frame1[i]->speed << endl;
        outfile << frame1[i]->direction[0] << " " << frame1[i]->direction[1] << endl;
        outfile << endl;
    }
    outfile << "end" << endl;
    outfile.close();
    
    infile0.close();
    infile1.close();
    return 0;
}

