<template>
  <div id="app" class="container">


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
        <button class="button is-info is-outlined" @click="scanForRegisterItem">Producer</button>
      </div>
      <div class="column has-text-centered">
          <button class="button is-info is-outlined">Super Market</button>
      </div>
      <div class="column has-text-centered">
          <button class="button is-info is-outlined" @click="verifyItem">Customer</button>
      </div>
    </div>

    <video id="preview"></video>


    <div class="columns is-mobile" v-show="isRegisterUser">
      <div class="column has-text-centered is-12">
        <div class="field">
          <label class="label">ONT ID</label>
          <div class="control">
            <input class="input" type="text" placeholder="did:ont:AJmgNXsSf9U9eddUY2JJB1F1fsuk3uMUUj" v-model="ont_id">
          </div>
          <label class="label">Position</label>
          <div class="control">
            <input class="input" type="text" placeholder="Tokyo Farm" v-model="position">
          </div>
        </div>
        <button class="button is-primary" @click="registerUser">Register</button>
      </div>
    </div>
  </div>
</template>

<script>
  /* eslint-disable no-undef */
  import { Identity, Crypto, OntidContract, RestClient, CONST, Account, TransactionBuilder, utils } from 'ontology-ts-sdk'
  import { client } from 'ontology-dapi'

  client.registerClient({})

  // wallet

  const scriptHash = 'f600cfbfdf794f2aa39d0eafe7bef0c72838cc82'

export default {
    name: 'app',
    data: function () {
      return {
        ont_id: '',
        position: '',
        mode: 'registerUser',
        isRegisterUser: true
      }
    },
    methods: {
      verifyItem () {
        this.isRegisterUser = false
        let scanner = new Instascan.Scanner({ video: document.getElementById('preview') })
        scanner.addListener('scan', async function (uuid) {
          console.log(uuid)
          alert(uuid)
          await scanner.stop()
  
          const operation = 'getItem'
          const args = [{ type: 'String', value: uuid }]
          console.log(args)
          const gasPrice = 500
          const gasLimit = 30000

          const result = await client.api.smartContract.invokeRead({ scriptHash, operation, args, gasPrice, gasLimit })
          console.log(result)
        })
        Instascan.Camera.getCameras().then(function (cameras) {
          if (cameras.length > 0) {
            scanner.start(cameras[0])
          } else {
            console.error('No cameras found.')
          }
        }).catch(function (e) {
          console.error(e)
        })
      },
      scanForRegisterItem () {
        this.isRegisterUser = false
  
        let scanner = new Instascan.Scanner({ video: document.getElementById('preview') })
        scanner.addListener('scan', async function (uuid) {
          console.log(uuid)
          alert(uuid)

          // register ONT ID

          const password = 'hogefuga'
          const label = 'test'
          const privateKey = Crypto.PrivateKey.random()

          const identity = Identity.create(privateKey, password, label)
          console.log(identity.toJson())

          const did = identity.ontid
          // we need the public key, which can be generate from private key
          const pk = privateKey.getPublicKey()
          const gasPrice = '500'
          const gasLimit = '20000'
          const tx = OntidContract.buildRegisterOntidTx(did, pk, gasPrice, gasLimit)

          const jsonStr = '{"address":"AM9GbRDpqHgbqrGDZNzgPaB6aGDVpsguc7","label":"test","lock":false,"algorithm":"ECDSA","parameters":{"curve":"P-256"},"key":"EFv1tEiQN5aeLaV+ecu9gn2I6cBSn6gMlUrO43To3G0mJ85+tGFGFGuW/doeP0Ee","enc-alg":"aes-256-gcm","hash":"sha256","salt":"/IoiUsK8WdLafyJj8rJTfg==","isDefault":false,"publicKey":"037788013ccd0eaa8e44379635ef3d8fe5dde96ca65743ab1ceab21991fbbe2cda","signatureScheme":"SHA256withECDSA"}'
          const account = Account.parseJson(jsonStr)

          tx.payer = account.address
          // First, we need sign transaction with the private key of the ONT ID.
          TransactionBuilder.signTransaction(tx, privateKey)
          // Then sign the transaction with payer's account
          // we already got transaction created before,add the signature.

          TransactionBuilder.addSign(tx, account.exportPrivateKey(password))
          const rest = new RestClient(CONST.TEST_ONT_URL.REST_URL)
          const res = await rest.sendRawTransaction(tx.serialize())
          console.log(`ont_id_register`)
          console.log(res)

          // ONT ID REGISTER END

          const operation = 'RegisterItem'
          const args = [{type: 'String', value: 'did:ont:AJmgNXsSf9U9eddUY2JJB1F1fsuk3uMUUj'}, { type: 'String', value: identity.ontid }, { type: 'String', value: uuid }]
          console.log(args)
          // const gasPrice = 500
          // const gasLimit = 30000

          const result = await client.api.smartContract.invoke({ scriptHash, operation, args, gasPrice, gasLimit })
          console.log(result)
          await scanner.stop()
          const msg = utils.hexstr2str(result.result[1])
          console.log(result.result)
          alert(msg)
        })

        Instascan.Camera.getCameras().then(function (cameras) {
          if (cameras.length > 0) {
            scanner.start(cameras[0])
          } else {
            console.error('No cameras found.')
          }
        }).catch(function (e) {
          console.error(e)
        })
      },
      async registerUser () {
        const operation = 'RegisterUser'
        // 'did:ont:AJmgNXsSf9U9eddUY2JJB1F1fsuk3uMUUj'
        const args = [{ type: 'String', value: this.ont_id }, { type: 'String', value: this.position }]
        const gasPrice = 500
        const gasLimit = 30000

        const result = await client.api.smartContract.invoke({ scriptHash, operation, args, gasPrice, gasLimit })
        console.log(result)
        alert('success!')
      },
      async getItem (uuid) {
        const operation = 'getItem'
        const args = [{ type: 'String', value: uuid }]
        const gasPrice = 500
        const gasLimit = 30000

        const result = await client.api.smartContract.invoke({ scriptHash, operation, args, gasPrice, gasLimit })
        console.log(result)
      },
      async registerItem () {
        // user_id, _uuid
        const operation = 'RegisterItem'
        const args = [{ type: 'String', value: 'did:ont:AJmgNXsSf9U9eddUY2JJB1F1fsuk3uMUUj' }, { type: 'String', value: 'f60d7db1-e891-4149-abc6-7874a613605e' }]
        const gasPrice = 500
        const gasLimit = 30000

        const result = await client.api.smartContract.invoke({ scriptHash, operation, args, gasPrice, gasLimit })

        console.log(result)
        console.log(result.result)
        console.log(utils.hexstr2str(result.result[0]))
        console.log(result)
      },
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
      importID () {
        const jsonStr = '{"ontid":"did:ont:AJmgNXsSf9U9eddUY2JJB1F1fsuk3uMUUj","label":"test","lock":false,"isDefault":false,"controls":[{"id":"1","algorithm":"ECDSA","parameters":{"curve":"P-256"},"key":"mKoyub/TWWcmBpp1a219LQlLdMLvpMGnd9Jb2hse0wB3u56ohLDupf0LV172xa9G","address":"AJmgNXsSf9U9eddUY2JJB1F1fsuk3uMUUj","salt":"PhzgPJAa4mi2byzVLoqy5Q==","enc-alg":"aes-256-gcm","hash":"sha256","publicKey":"03b8ed33d1dba5c83a894dd3f2ba49bed272953b0d92e28e4ff748751e3035e45d"}]}'
        const id = Identity.parseJson(jsonStr)
        console.log(id)
      },
      createID2 () {
        const password = 'hogefuga'
        const label = 'test'
        const privateKey = Crypto.PrivateKey.random()

        const identity = Identity.create(privateKey, password, label)
        console.log(identity.toJson())

        const did = identity.ontid
        // we need the public key, which can be generate from private key
        const pk = privateKey.getPublicKey()
        const gasPrice = '500'
        const gasLimit = '20000'
        const tx = OntidContract.buildRegisterOntidTx(did, pk, gasPrice, gasLimit)

        const jsonStr = '{"address":"AM9GbRDpqHgbqrGDZNzgPaB6aGDVpsguc7","label":"test","lock":false,"algorithm":"ECDSA","parameters":{"curve":"P-256"},"key":"EFv1tEiQN5aeLaV+ecu9gn2I6cBSn6gMlUrO43To3G0mJ85+tGFGFGuW/doeP0Ee","enc-alg":"aes-256-gcm","hash":"sha256","salt":"/IoiUsK8WdLafyJj8rJTfg==","isDefault":false,"publicKey":"037788013ccd0eaa8e44379635ef3d8fe5dde96ca65743ab1ceab21991fbbe2cda","signatureScheme":"SHA256withECDSA"}'
        const account = Account.parseJson(jsonStr)

        tx.payer = account.address
        // First, we need sign transaction with the private key of the ONT ID.
        TransactionBuilder.signTransaction(tx, privateKey)
        // Then sign the transaction with payer's account
        // we already got transaction created before,add the signature.
  
        TransactionBuilder.addSign(tx, account.exportPrivateKey(password))
        const rest = new RestClient(CONST.TEST_ONT_URL.REST_URL)
        rest.sendRawTransaction(tx.serialize()).then(res => {
          console.log(res)
          alert('hoge')
        })
      },
      openCamera (e) {
        const node = e.toElement
        console.log(e)
        console.log(node)
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

