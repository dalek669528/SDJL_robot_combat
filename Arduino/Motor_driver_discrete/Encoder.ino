void Encoder_A(){
  if(digitalRead(SPD_INT_A2) == LOW){
    A.encoder = A.encoder + 1; //Forward
  }
  else{
    A.encoder = A.encoder - 1; //Reverse
  }
}

void Encoder_B(){
  if(digitalRead(SPD_INT_B2) == LOW){
    B.encoder = B.encoder + 1; //Forward
  }
  else{
    B.encoder = B.encoder - 1; //Reverse
  }
}

void Encoder_C(){
  if(digitalRead(SPD_INT_C2) == HIGH){
    C.encoder = C.encoder + 1; //Forward
  }
  else{
    C.encoder = C.encoder - 1; //Reverse
  }
}

void Encoder_D(){
  if(digitalRead(SPD_INT_D2) == HIGH){
    D.encoder = D.encoder + 1; //Forward
  }
  else{
    D.encoder = D.encoder - 1; //Reverse
  }
}
