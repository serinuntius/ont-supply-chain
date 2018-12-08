<template>
  <div id="app">

    <nav class="navbar" role="navigation" aria-label="main navigation">
      <div class="navbar-brand">
        <a class="navbar-item" href="https://bulma.io">
          <img src="https://bulma.io/images/bulma-logo.png" width="112" height="28">
        </a>

        <a role="button" class="navbar-burger burger" aria-label="menu" aria-expanded="false"
           data-target="navbarBasicExample">
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
        </a>
      </div>

      <div id="navbarBasicExample" class="navbar-menu">
        <div class="navbar-start">
          <a class="navbar-item">
            Home
          </a>

          <a class="navbar-item">
            Documentation
          </a>

          <div class="navbar-item has-dropdown is-hoverable">
            <a class="navbar-link">
              More
            </a>

            <div class="navbar-dropdown">
              <a class="navbar-item">
                About
              </a>
              <a class="navbar-item">
                Jobs
              </a>
              <a class="navbar-item">
                Contact
              </a>
              <hr class="navbar-divider">
              <a class="navbar-item">
                Report an issue
              </a>
            </div>
          </div>
        </div>

        <div class="navbar-end">
          <div class="navbar-item">
            <div class="buttons">
              <a class="button is-primary">
                <strong>Sign up</strong>
              </a>
              <a class="button is-light">
                Log in
              </a>
            </div>
          </div>
        </div>
      </div>
    </nav>

    <div id="role-selector" class="columns is-mobile">
      <div class="column has-text-centered">
        <button class="button is-info is-outlined">Producer</button>
      </div>
      <div class="column has-text-centered">
        <button class="button is-info is-outlined">Super Market</button>
      </div>
      <div class="column has-text-centered">
        <button class="button is-info is-outlined">Customer</button>
      </div>
    </div>
    <div class="columns">
      <div class="column is-12">
      </div>
    </div>

    <div class="columns is-mobile">
      <div class="column has-text-centered">
        <button class="button is-primary">
         <span id="camera-icon">
           <i class="fas fa-camera"></i>
         </span> Scan
          <input type=file accept="image/*" capture=environment @click="openCamera(this)" onchange="" tabindex=-1>
        </button>
        <button class="button is-primary" @click="createID">
          create id
        </button>
        <button class="button is-primary" @click="createAccount">
          create Account
        </button>
        <button class="button is-primary" @click="importAccount">
          import Account
        </button>
      </div>
    </div>
  </div>
</template>

<script>
  /* eslint-disable no-undef */

  import {Identity, Crypto, OntidContract, RestClient, CONST, Account} from 'ontology-ts-sdk'

  // wallet

  export default {
    name: 'app',
    methods: {
      createAccount () {
        const keyParameters = new Crypto.KeyParameters(Crypto.CurveLabel.SECP256R1)
        console.log(keyParameters)
        const privateKey = Crypto.PrivateKey.random(Crypto.KeyType.ECDSA, keyParameters)
        console.log(privateKey)
        const account = Account.create(privateKey, 'hogefuga', 'test')
        console.log(account.toJson())
        return account
      },
      importAccount () {
        const jsonStr = '{"address":"AM9GbRDpqHgbqrGDZNzgPaB6aGDVpsguc7","label":"test","lock":false,"algorithm":"ECDSA","parameters":{"curve":"P-256"},"key":"EFv1tEiQN5aeLaV+ecu9gn2I6cBSn6gMlUrO43To3G0mJ85+tGFGFGuW/doeP0Ee","enc-alg":"aes-256-gcm","hash":"sha256","salt":"/IoiUsK8WdLafyJj8rJTfg==","isDefault":false,"publicKey":"037788013ccd0eaa8e44379635ef3d8fe5dde96ca65743ab1ceab21991fbbe2cda","signatureScheme":"SHA256withECDSA"}'
        const account = Account.parseJson(jsonStr)
        console.log(account)
        return account
      },
      createID () {
        // generate a random private key
        // const privateKey = Crypto.PrivateKey.random()
        // console.log(privateKey)
        const password = 'hogefuga'
        // const label = 'test'

        // const identity = Identity.create(privateKey, password, label)
        const identity = Identity.parseJson('{"ontid":"did:ont:AaXidkKV9HrR5dxTJ4WNkg19NSRyc5AHf7","label":"test","lock":false,"isDefault":false,"controls":[{"id":"1","algorithm":"ECDSA","parameters":{"curve":"P-256"},"key":"QZ0U2wiPaMquYyaeA1aFXVXz9gMvry3kwspdT1HOMVKqJEmeaoRZ80xn3N0jigfp","address":"AaXidkKV9HrR5dxTJ4WNkg19NSRyc5AHf7","salt":"d4UIuQZ9q6JghFc7eFzZhQ==","enc-alg":"aes-256-gcm","hash":"sha256","publicKey":"02c3544b8ea736920e7d158349144f7cbe08996ca3b685fa79b11c4776518518be"}]}')
        console.log(identity.toJson())
        console.log(identity.ontid)
        const did = identity.ontid

        console.log(identity.controls[0].address)
        const _pk = identity.controls[0].publicKey
        const pk = new Crypto.PublicKey(_pk)

        // const pk = privateKey.getPublicKey()
        // console.log(pk)
        const gasPrice = '500'
        const gasLimit = '20000'
        const tx = OntidContract.buildRegisterOntidTx(did, pk, gasPrice, gasLimit)
        identity.signTransaction(password, tx)

        // TransactionBuilder.signTransaction(tx, privateKey)
  
        /* const jsonStr = '{"address":"AM9GbRDpqHgbqrGDZNzgPaB6aGDVpsguc7","label":"test","lock":false,"algorithm":"ECDSA","parameters":{"curve":"P-256"},"key":"EFv1tEiQN5aeLaV+ecu9gn2I6cBSn6gMlUrO43To3G0mJ85+tGFGFGuW/doeP0Ee","enc-alg":"aes-256-gcm","hash":"sha256","salt":"/IoiUsK8WdLafyJj8rJTfg==","isDefault":false,"publicKey":"037788013ccd0eaa8e44379635ef3d8fe5dde96ca65743ab1ceab21991fbbe2cda","signatureScheme":"SHA256withECDSA"}'
        const account = Account.parseJson(jsonStr)
        console.log(`address: ${account.address.value}`)

        tx.payer = account.address
        const signedTx = account.signTransaction('hogefuga', tx)
        // TransactionBuilder.addSign(tx, privateKeyOfAccount)

        */

        const rest = new RestClient(CONST.TEST_ONT_URL.REST_URL)
        rest.sendRawTransaction(tx.serialize()).then(res => {
          console.log(res)
          alert('hoge')
        })
      },
      openCamera (node) {
        const reader = new FileReader()
        reader.onload = function () {
          qrcode.callback = function (res) {
            if (res instanceof Error) {
              alert("No QR code found. Please make sure the QR code is within the camera's frame and try again.")
            } else {
              alert(res)
            }
          }
          qrcode.decode(reader.result)
        }
        reader.readAsDataURL(node.files[0])
      }
    }
  }
</script>

<style scoped>
  #role-selector {
    padding-top: 30px;
  }

  #camera-icon {
    padding-right: 15px;
  }
</style>

