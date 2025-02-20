<script setup>
import { upload, getText } from './composables/useAPI'
import { ref } from 'vue'
import { ElMessage } from 'element-plus'

const form = ref({
});

// for upload
const text_upload = ref('')
const if_one_time = ref(false)
const expire_time = ref(0)
const access_limit = ref(1)

const ramdom_code_get = ref('Waiting for response')

// for get
const ramdom_code_send = ref('ToDo')
const res_text = ref('Waiting for response')

const status_bar = ref('...')

async function submit() {
  try {
    const { res, status } = await upload(text_upload.value, if_one_time.value, expire_time.value, access_limit.value)
    console.log(res, status)
    ramdom_code_get.value = res.data
    status_bar.value = status
    console.log(`Get submit res: ${ramdom_code_get.value}, Status: ${status_bar.value}`)
  } catch (err) {
    status_bar.value = err
    console.log(err)
  }
}

async function get() {
  const { res, status } = await getText(ramdom_code_send.value)
  res_text.value = res.data
  status_bar.value = status
}

function clear() {
  ramdom_code_get.value = 'Waiting for response'
  ramdom_code_send.value = 'ToDo'
  res_text.value = 'Waiting for response'
  status_bar.value = '...'
  text_upload.value = ''
}

function copyCode() {
  const code = ramdom_code_get.value;
  navigator.clipboard.writeText(code).then(() => {
    ElMessage.success('Code is copied to clipboard');
  }).catch(err => {
    ElMessage.error('Failed to copy code: ' + err);
  });
}

function pasteCode() {
  navigator.clipboard.readText().then(code => {
    ramdom_code_send.value = code;
  }).catch(err => {
    ElMessage.error('Failed to paste code: ' + err);
  });
}

function copyRes() {
  const res = res_text.value;
  navigator.clipboard.writeText(res).then(() => {
    ElMessage.success('Code is copied to clipboard');
  }).catch(err => {
    ElMessage.error('Failed to copy code: ' + err);
  });
}
</script>
<!-- ============= Script & Template ============= -->

<template>
  <el-container>
    <el-main>

      <el-card style="display: flex; justify-content: center; align-items: center; text-align: center; ">
        <div style="font-weight: bold; font-size: xx-large;">
          Welcome!
        </div>
        <span>{{ status_bar }}</span>
      </el-card>

      <el-row :gutter="20" style="display: flex; justify-content: space-between; align-items: stretch;">
        <!-- Save -->
        <el-col :span="12" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
          <el-card style="width: 100%; height: 100%;">
            <el-form :model="form" label-width="120px" style="margin-top: 10px;" label-position="left">

              <h3>Save to Clipboard</h3>

              <el-form-item label="Input Text">
                <el-input type="textarea" aria-required="true" v-model="text_upload" placeholder="Please input your text" :rows="3"></el-input>
              </el-form-item>

              <el-form-item label="Expire(min)">
                <el-input-number v-model="expire_time" :min="1"></el-input-number>
              </el-form-item>

              <el-form-item label="Access Limit">
                <el-input-number v-model="access_limit" :min="1"></el-input-number>
              </el-form-item>

              <el-form-item label="Your Code" style="display: flex; align-items: center;">
                <span class="span_shadow" style="margin-right: 10px;">{{ ramdom_code_get }}</span>
                <el-button type="primary" @click="copyCode">Copy</el-button>
              </el-form-item>

              <el-form-item label="If-One-Time">
                <el-checkbox v-model="if_one_time"></el-checkbox>
              </el-form-item>

              <el-form-item>
                <el-row :gutter="10">
                  <el-col :span="12">
                    <el-button type="primary" @click="submit">Submit</el-button>
                  </el-col>
                  <el-col :span="12">
                    <el-button type="info" @click="clear">Clear</el-button>
                  </el-col>
                </el-row>
              </el-form-item>

            </el-form>
          </el-card>
        </el-col>

        <!-- Fetch -->
        <el-col :span="12" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
          <el-card style="width: 100%; height: 100%;">
            <h3>Fetch from Clipboard</h3>

            <el-form :model="form" label-width="120px" style="margin-top: 10px;" label-position="left">

              <el-form-item label="Code" style="display: flex; align-items: center;">
                <el-input v-model="ramdom_code_send" placeholder="Enter your code"
                  style="flex: 1; margin-right: 10px;"></el-input>
                <el-button type="primary" @click="pasteCode">Paste</el-button>
              </el-form-item>

              <el-form-item label="Result">
                <el-input type="textarea" v-model="res_text" :rows="8" readonly></el-input>
              </el-form-item>

              <el-form-item>
                <el-row :gutter="10">
                  <el-col :span="8">
                    <el-button type="primary" @click="get" style="width: 100%;">Get</el-button>
                  </el-col>
                  <el-col :span="8">
                    <el-button type="primary" @click="copyRes" style="width: 100%;">Copy</el-button>
                  </el-col>
                  <el-col :span="8">
                    <el-button type="info" @click="clear" style="width: 100%;">Clear</el-button>
                  </el-col>
                </el-row>
              </el-form-item>
            </el-form>

          </el-card>
        </el-col>
      </el-row>

    </el-main>

  </el-container>
</template>

<style scoped></style>
