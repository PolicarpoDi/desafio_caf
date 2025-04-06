## Companies

```
[
  '{{repeat(10)}}',
  {
    _id: '{{objectId()}}',
    fantasyName: '{{company()}}',
    cnpj: '{{email()}}',
    status: '{{random("Ativo", "Inativo")}}',
    segment: '{{random("Banco", "Ecommerce", "Serviços")}}'
  }
]
```


## Users
```
[
  '{{repeat(100)}}',
  {
    _id: '{{objectId()}}',
    name: '{{firstName()}} {{surname()}}',
    email: '{{email(true)}}',
    createdAt: '{{date(new Date(2020, 0, 1), new Date(), "YYYY-MM-ddThh:mm:ss Z")}}',
    birthdate: '{{date(new Date(1980, 0, 1), new Date(1999, 0, 1), "YYYY-MM-ddThh:mm:ss Z")}}'
  }
]
```

## Transactions
```
[
  '{{repeat(10000)}}',
  {
    _id: '{{objectId()}}',
    tenantId: '{{random("64132ef6526eeb8b998e2d3c","64132ef6f991a3a1884f2cd0","64132ef6dca9067d51ca1b30","64132ef6eea665cc154f614a","64132ef662f97d5858f87aba","64132ef6f54b06e1ffb65fba","64132ef64f72ae4d32dc3535","64132ef6ccd2d35a83c3544a","64132ef6c9c22c95893e388b","64132ef68637da8c371cdc09")}}',
    userId: '{{random("64132e0fa1b98612a1366a0a","64132e0f90329937be6d5b65","64132e0f429adbbe0334ad00","64132e0f05e9b1d120893ffe","64132e0f483bdb42b75e860c","64132e0f9bbde2888d09e570","64132e0f8ad64890298e4d1e","64132e0f0c020ecd45aea2db","64132e0f05f9e9ca1e250a65","64132e0f7592c8eadca451f9","64132e0fc7534e992bafa834","64132e0f7847d1ad65a92102","64132e0fb4fade825fdbeed4","64132e0f48ad8ae93e504d33","64132e0fc77ec324b4a3b1d6","64132e0fb3add2bba99bcb24","64132e0f25f70db60e2eeb8e","64132e0f72bb82a25ea19ecb","64132e0fb3c06ddc6c896f5b","64132e0fa078fea397f180eb","64132e0f022a91f2806aaefe","64132e0f8e3082f0517fdfdb","64132e0f9417d076f85b8f61","64132e0f21cc4fc3bf2da26f","64132e0f8b3d3810100355b5","64132e0f63c1a33ae32d7a99","64132e0f76b4e9b5fc6496c6","64132e0ff31bfea3ecc4d0b6","64132e0f19d8c115ba93536c","64132e0ff7c0a95b1a0707b0","64132e0f8df1cb7b954fecf9","64132e0fb611e00924b0b8e0","64132e0f16e8266d4823236c","64132e0fec1b702b2378c379","64132e0f708218333d413c4c","64132e0fddc4fe73fd258a24","64132e0f38c6485f069d4421","64132e0fe0f83495969d409d","64132e0f1d87f017f64a3c20","64132e0fccaa6cd8f625d942","64132e0f95dc386b40202460","64132e0f861fcfbc0c1ca217","64132e0f7dc97b755f68884d","64132e0f6ed08d9ca49a70c4","64132e0faa55e10ce7ee68a3","64132e0fe57d5c5c32addeec","64132e0f407b51b8b5dc2dba","64132e0f68da4c705b3b80e0","64132e0f4884b463e3fa4bb5","64132e0f3e421185043a4e7b","64132e0f0bda9c4ebba64c82","64132e0f74cda6acaa908563","64132e0fa397563115444821","64132e0f5dcfd2856d9f8337","64132e0fe14d128d168160e4","64132e0f9647ed73a005c271","64132e0f5aa12367ada0a118","64132e0fe7a0ca7f994cca17","64132e0f555673bb72251b1d","64132e0fa5ce9da5cb51ed97","64132e0fdecad60766d8ab2c","64132e0fd3bdca816cd9ac2f","64132e0f63537c3b711d2a83","64132e0f6f7f7af7c4dfe156","64132e0f00e22f4ac7b67520","64132e0fc26ed10af69ef2e3","64132e0fd9d750210c1746a1","64132e0f58ce216e866593d6","64132e0ff99f08aa40f089ae","64132e0fac889c7cbd7ebda3","64132e0ffe16938ae5708fb3","64132e0f29d8b74c6b1cb514","64132e0fbfc9f83e9c20d1a2","64132e0f67e98be3094ec5c9","64132e0f56dd370a14cd262a","64132e0fe8e5688a81c56b8a","64132e0fd287835096499eed","64132e0f7aee8254eafaa63a","64132e0f60176a0a0afefe23","64132e0feb28dcda49522904","64132e0f7da24bcd8d8ca3fb","64132e0f0abcd78da3792cfe","64132e0fa9c7a5c639898a57","64132e0fc8ad114d29212998","64132e0f72148c806c32b064","64132e0fc615332b14dfbd62","64132e0f85b016750b1e4f8e","64132e0fd91959d4e9a0bd8b","64132e0f1c3cdc367a6667aa","64132e0fcc5c3bf2d6217765","64132e0ff24b4a855793a5cf","64132e0fbb8283fc0ab24791","64132e0f56a8e4996c9497b4","64132e0f35c0faf75c5ad3e1","64132e0f8ae9531161eb5f9d","64132e0fd0fd03a2161eade3","64132e0f5db21511f29bd2c3","64132e0f49625262850d71ab","64132e0f1eeec2acd297c0e9","64132e0ff769e21f3707d966")}}',
    createdAt: '{{date(new Date(2021, 0, 1), new Date(2023, 0, 1), "YYYY-MM-ddThh:mm:ss Z")}}',
    updatedAt: '{{date(new Date(2023, 0, 2), new Date(), "YYYY-MM-ddThh:mm:ss Z")}}',
    favoriteFruit: function (tags) {
      var fruits = ['apple', 'banana', 'strawberry'];
      return fruits[tags.integer(0, fruits.length - 1)];
    },
    isFraud: '{{bool()}}',
    document: {
      documentType: '{{random("RG", "CNH", "CTPS")}}',
      documentUF: '{{random("SP", "RJ", "RS", "BA", "PA", "MT")}}'
    }
  }
]
```