import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatBasicComponent } from './mat-basic/mat-basic.component';
import { MatDialogModule } from '@angular/material/dialog';
import { MatButtonModule } from '@angular/material/button';

@NgModule({
  declarations: [
    MatBasicComponent
  ],
  imports: [
    CommonModule,
    MatDialogModule,
    MatButtonModule,
  ], exports: [
    MatDialogModule,
    MatButtonModule
  ]
})
export class NgMaterialModule { }
