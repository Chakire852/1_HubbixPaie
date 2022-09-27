import { Component, OnInit } from '@angular/core';


@Component({
  selector: 'app-mat-basic',
  templateUrl: './mat-basic.component.html',
  styleUrls: ['./mat-basic.component.scss']
})
export class MatBasicComponent implements OnInit {

  message1: string;
  message2: string;
  message3: string;
  buttonText: string;

  constructor() { }

  setInfo(data) {
    this.message1 = data.message1;
    this.message2 = data.message2;
    this.message3 = data.message3;
    this.buttonText = data.buttonText;
  }

  ngOnInit() {
  }

}
