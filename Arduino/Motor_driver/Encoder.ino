void Encoder_A(){
  if(digitalRead(SPD_INT_A2) == LOW)
    car.A.encoder = car.A.encoder + 1; //Forward
  else
    car.A.encoder = car.A.encoder - 1; //Reverse
}

void Encoder_B(){
  if(digitalRead(SPD_INT_B2) == LOW)
    car.B.encoder = car.B.encoder + 1; //Forward
  else
    car.B.encoder = car.B.encoder - 1; //Reverse
}

void Encoder_C(){
  if(digitalRead(SPD_INT_C2) == HIGH)
    car.C.encoder = car.C.encoder + 1; //Forward
  else
    car.C.encoder = car.C.encoder - 1; //Reverse
}

void Encoder_D(){
  if(digitalRead(SPD_INT_D2) == HIGH)
    car.D.encoder = car.D.encoder + 1; //Forward
  else
    car.D.encoder = car.D.encoder - 1; //Reverse
}
