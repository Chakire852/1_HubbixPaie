import { Router } from '@angular/router';
import { Component, OnInit, OnDestroy } from '@angular/core';
import { Document } from '../models/document';
import { HomeService } from '../services/home/home.service';
import { VerseService } from '../manager.service';
import { MatDialog } from '@angular/material/dialog';
import { DomSanitizer } from '@angular/platform-browser';
import { MatBasicComponent } from '../ng-material/mat-basic/mat-basic.component';
//import { NgMaterialModule } from '../ng-material/ng-material.module';
import { Subscription } from "rxjs";

@Component({
  selector: 'app-document',
  templateUrl: './document.component.html',
  styleUrls: ['./document.component.scss']
})
export class DocumentComponent implements OnInit, OnDestroy {

  Documents: Document[] = [];
  docId: string;
  docName: string;
  docDate: any;
  status: string;
  operation: string;

  public loading: boolean = false;
  public loadingSubscription: Subscription;

  constructor(private router: Router,
              private verseService: VerseService,
              private homeService: HomeService,
              private domSanitizer: DomSanitizer,
              public dialog: MatDialog
              ) { }

  ngOnInit() {
    this.loadingSubscription = this.homeService.loadingStatus.subscribe((value) => {
      this.loading = value;
    });
    this.verseService.getAllDocuments().subscribe(objs => {
      this.Documents = objs;
    });
  }

  gotoDetails(docId: any, date: any, name: any, processed: any) {
    this.router.navigate(['/listArticles/', docId], {
      queryParams: {
        name: name,
        date: date,
        processed: processed
      }
    });
  }

  deleteDocument(docId: any, name: any) {
    this.docId = docId;
    this.docName = name;
    this.operation = 'Delete';
    this.openDialog('Supprimer',
                    'Confirmez vous la suppresion du document',
                    name,
                    'et de tous les articles associés ?');
    
  }

  goNLP(docId: any, name: any, date: any) {
    this.docId = docId;
    this.docName = name;
    this.docDate = date;
    this.operation = 'NLP';
    this.openDialog('Démarrer',
      'Voulez-vous démarrer le traitement par NLP des articles du',
      name + ' ?',
      'Cette procèdure pourrait être longe, et vous ne pourriez pas utiliser le système pendant toute la durée de l\'opération');
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
        switch (this.operation) {
          case 'Delete': this.deleteContent(this.docId); break;
          case 'NLP': this.nlpDocument(this.docId); break;
          default: break;
        }
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

  nlpDocument(doc_id) {
    this.verseService.nlpDocument(doc_id).subscribe(() =>
      this.gotoDetails(doc_id, this.docDate, this.docName, true)
    );
  }

  ngOnDestroy() {
    this.loadingSubscription.unsubscribe();
  }

  sanitize(url: string) {
    return this.domSanitizer.bypassSecurityTrustUrl(url);
  }
}
