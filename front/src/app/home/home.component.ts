import { Component, OnDestroy, OnInit } from '@angular/core';
import { HomeService } from '../services/home/home.service'
import { VerseService } from '../manager.service';
import { DomSanitizer } from '@angular/platform-browser';
import { MatDialog } from '@angular/material/dialog';
import { MatBasicComponent } from '../ng-material/mat-basic/mat-basic.component';
import { NgMaterialModule } from '../ng-material/ng-material.module';
import { Document } from '../models/document';
import { Subscription } from "rxjs";

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit, OnDestroy {

  public codesLegifrance;
  public loading: boolean = false;
  public loadingSubscription: Subscription;

  private doc_id: string;
  private doc_exists: boolean;
  private status;
  private document;

  constructor(private verseService: VerseService,
              private domSanitizer: DomSanitizer,
              public dialog: MatDialog,
              public module: NgMaterialModule,
              private homeService: HomeService,
             ) {
  }

  ngOnInit() {
    this.loadingSubscription = this.homeService.loadingStatus.subscribe((value) => {
      this.loading = value;
    });
    this.verseService.getCodes().subscribe(objs => {
      this.codesLegifrance = objs;
    });
  }

  ngOnDestroy() {
    this.loadingSubscription.unsubscribe();
  }

  sanitize(url: string) {
    return this.domSanitizer.bypassSecurityTrustUrl(url);
  }

  CheckDocumentById(doc_id: string) {
    this.doc_id = doc_id;
    this.verseService.checkDocument(doc_id).subscribe(
      (result) => {
        this.doc_exists = true;
        var document: Document = result;
        var name : string = document.name;
        var date = new Date(document.date).toLocaleDateString('fr-FR');
        this.openDialog('Télécharger',
                        'Le fichier ' + name,
                        'existe déjà en la base de données, daté du ' + date + '.',
                        'Voulez-vous le télécharger à nouveau ? Cette procedure peut être longue');
      },
      () => {
        this.doc_exists = false
        this.openDialog('Télécharger', 'Voulez-vous télécharger ce fichier ? Cette procedure peut être longue');
    })
  }

  openDialog(buttonText, message1, message2?, message3?) {
    const dialogRef = this.dialog.open(MatBasicComponent);
    dialogRef.componentInstance.setInfo({
      message1: message1,
      message2: message2,
      message3: message3,
      buttonText: buttonText
      })
    
    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        if (this.doc_exists) {
          this.deleteContent(this.doc_id);
        }
        this.verseService.downloadCodeById(this.doc_id).subscribe(() => {
          this.status = 'Content downloaded';
        });
        console.log('Content downloaded');

        this.saveContent(this.doc_id);
      }
    });
  }

  deleteContent(doc_id) {
    this.verseService.deleteArticles(doc_id).subscribe(() =>
      this.status = 'Articles deleted'
    )
    this.verseService.deleteDocument(doc_id).subscribe(() =>
      this.status = 'Document deleted'
    );
    console.log('Content Deleted');
  }

  saveContent(doc_id) {
    this.verseService.saveDocumentInBd().subscribe((objs) => {
      this.doc_id = objs;
      this.status = "Document saved";
    });
    this.verseService.saveArticlesInBd(doc_id).subscribe(() => {
      this.status = "Articles saved";
    });
  }
}
