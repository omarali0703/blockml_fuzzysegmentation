//float x,y,z;
float rotateI;
String[] data;

float[][] trainingData;
float moveX, moveY;
void setup() {
  size(600, 600, P3D);
  noStroke();

  data = loadStrings("train_0_k5.dat");
  trainingData = new float[data.length][4];
  for (int i = 0; i < data.length; i ++) {
    String lineElement = data[i];
    String[] values = split(lineElement, ' ');
    float[] row = new float[4];
    row[0]=float(values[0]);
    row[1]=float(values[1]);
    row[2]=float(values[2]);
    row[3]=float(values[3]);

    trainingData[i] = row;
  }
}
float xx, yy, zz;
void draw() {
  background(0xffffff);
  //rotateY(PI/4);
  //rotateZ(PI/4);
  //rotateY(mouseX*0.005);
  translate(width/2, height/2, 0);
    translate(moveX, moveY, 0);

  rotateZ(radians(zz));
  rotateY(radians(yy));
  rotateX(radians(xx));
  //translate(mouseX,mouseY, 0);
  int scale = 200;
  stroke(220);
  pushMatrix();
  line(0, 0, 0, scale, 0, 0);
  line(0, 0, 0, 0, scale, 0);
  line(0, 0, 0, 0, 0, scale);
  popMatrix();
  pushMatrix();
  translate(scale + 10, 0, 0);
  rotateX(-PI/4);
  text("int_coh_i", 0, 0, 0);
  popMatrix();
  pushMatrix();
  translate(0, scale + 10, 0);
  rotateX(-PI/4);
  text("int_coh_j", 0, 0, 0);
  popMatrix();
  pushMatrix();
  translate(0, 0, scale + 10);
  rotateX(-PI/4);
  text("ext_diss", 0, 0, 0);
  popMatrix();
  noStroke();
  for (int i = 0; i < trainingData.length; i++) {
    pushMatrix();
    float [] dataElement = trainingData[i];
    float col = dataElement[0] == 1 ? 51 : 200;
    float x = dataElement[1];
    float y = dataElement[2];
    float z = dataElement[3];

    translate(x*scale, y*scale, z*scale);

    fill(col);
    //stroke(255);
    rectMode(CENTER);
    //circle(0, 0, 2);
    sphere(2);
    translate(0, 0, 0);

    popMatrix();
    //yy += 20;
    if (keyPressed) {
      if (key == 'a' || key == 'A') {
        yy += 0.05;
      } else if (key == 'd' || key == 'D') {
        yy -= 0.05;
      } else if (key == 'a' || key == 'D') {
        yy -= 0.05;
      } else if (key == 'w' || key == 'W') {
        xx -= 0.05;
      } else if (key == 's' || key == 'S') {
        xx += 0.05;
      } else if (key == 'f' || key == 'F') {
        moveX -= 0.05;
      } else if (key == 'h' || key == 'H') {
        moveX += 0.05;
      } else if (key == 't' || key == 'T') {
        moveY -= 0.05;
      } else if (key == 'G' || key == 'g') {
        moveY += 0.05;
      }
    }
  }

  //noLoop();
}
