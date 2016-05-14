/**
 * @license Copyright (c) 2003-2015, CKSource - Frederico Knabben. All rights reserved.
 * For licensing, see LICENSE.md or http://ckeditor.com/license
 */

CKEDITOR.editorConfig = function( config ) {
	// Define changes to default configuration here. For example:
	// config.language = 'fr';
	// config.uiColor = '#AADC6E';
	config.height = 500;
	config.toolbar = [
		{ name: 'basicstyles', items: [ 'Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript' ] },
		{ name: 'styles', items: [ 'Format' ] },
		{ name: 'paragraph', items: [ 'Blockquote', 'NumberedList', 'BulletedList' ] },
		{ name: 'insert', items: [ 'HorizontalRule', 'Smiley', 'SpecialChar' ] },
		{ name: 'paragraph', items: [ 'Outdent', 'Indent', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'BidiLtr', 'BidiRtl' ] },
		{ name: 'colors', items: [ 'TextColor', 'BGColor' ] },
		{ name: 'clipboard', items: [ 'Undo', 'Redo' ] },
		{ name: 'basicstyles', items: [ 'RemoveFormat' ] },
		{ name: 'editing', items: [ 'SelectAll' ] },
		{ name: 'tools', items: [ 'Maximize' ] },
	];
};
